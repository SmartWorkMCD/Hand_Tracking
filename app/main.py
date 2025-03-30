import json
import cv2
import mediapipe as mp
import numpy as np
import threading
import time
from comms import init_broker, connect_broker , Hands_Information
from config import config , log_message

stop_flag = False
mp_hands = None
mp_drawing = None
hands = None

def on_message(client, userdata, msg):
    global stop_flag
    """ Callback function to handle incoming messages. """
    message_payload = msg.payload.decode("utf-8")
    hand_msg: Hands_Information = Hands_Information().from_json(message_payload)
    log_message(f"Received message on {msg.topic}: {hand_msg.timestamp}")
    del hand_msg

def consumer():
    """ Initializes and starts the MQTT consumer. """
    global stop_flag
    client = init_broker()
    client.on_message = on_message 
    connect_broker(client)
    client.subscribe(config.BROKER_TOPIC)
    log_message(f"Subscribed to topic: {config.BROKER_TOPIC}, waiting for messages...")
    
    while not stop_flag:
        client.loop(timeout=0.1)
    
    client.disconnect()
    log_message("Consumer thread exiting...")

def process_frame(frame):
    """ Processes a single frame to detect hand landmarks and calculate pointing angle. """
    global mp_hands, mp_drawing, hands
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(frame)

    h, w, _ = frame.shape
    hand_msg = None
    if hand_results.multi_hand_landmarks:
        hand_msg = Hands_Information()
        for i, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
            # get handedness (left or right hand)
            handedness = hand_results.multi_handedness[i].classification[0].label
                                
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            # Convert to pixel coordinates
            wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)
            index_x, index_y = int(index_mcp.x * w), int(index_mcp.y * h)
            # Estimate forearm direction based on hand orientation
            delta_x = wrist_x - index_x
            delta_y = wrist_y - index_y
            # Calculate the hand pointing angle
            angle_deg = np.degrees(np.arctan2(delta_y, delta_x))
            # Adjust the angle for North (0 degrees = up)
            pointing_angle = 90 - angle_deg  # 0 degrees is north (upward)
            if pointing_angle < 0:
                pointing_angle += 360  # Normalize to [0, 360)

            hand_msg.add_hand(hand_landmarks, handedness, pointing_angle)

            if config.SHOW_SCREEN:
                # Draw the forearm
                forearm_length = 100
                norm = np.sqrt(delta_x**2 + delta_y**2)
                delta_x = (delta_x / norm) * forearm_length
                delta_y = (delta_y / norm) * forearm_length
                # Estimate elbow position
                elbow_x = int(wrist_x + delta_x)
                elbow_y = int(wrist_y + delta_y)
                # Draw everything
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) # Draw hand connections
                cv2.circle(frame, (wrist_x, wrist_y), 10, (0, 255, 0), -1) # Green dot for wrist
                cv2.line(frame, (wrist_x, wrist_y), (elbow_x, elbow_y), (0, 255, 255), 4) # Yellow line for forearm
                cv2.circle(frame, (elbow_x, elbow_y), 10, (0, 0, 255), -1) # Red dot for elbow
    if config.SHOW_SCREEN:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
    return hand_msg

def main():
    """ Runs both producer and consumer. """
    global stop_flag , mp_hands, mp_drawing, hands
    
    if config.PRODUCER_ECHO:
        log_message("Starting consumer thread...")
        consumer_thread = threading.Thread(target=consumer, daemon=True)  # Daemon thread keeps running
        consumer_thread.start()

    client = init_broker()
    connect_broker(client)
    
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(config.CAMERA_ID)
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    if mp_hands is None or hands is None or mp_drawing is None:
        log_message("Failed to initialize MediaPipe Hands", level="ERROR")
        return
    
    if not cap.isOpened():
        log_message("Failed to open camera", level="ERROR")
    
    try:
        while cap.isOpened():
            s_time = time.time()
            ret , frame = cap.read()
            
            if not ret:
                log_message("Failed to capture frame",level="ERROR")
                break
            
            if config.FLIP_CAMERA_H:
                frame = cv2.flip(frame, 1)
            if config.FLIP_CAMERA_V:
                frame = cv2.flip(frame, 0)
                
            hand_msg =  process_frame(frame)
            
            if hand_msg is not None:
                hand_msg.timestamp = time.time()
                json_str = hand_msg.to_json()
                client.publish(config.BROKER_TOPIC, json_str)
              
            time.sleep(max(0, (1 / config.TARGET_FPS) - (time.time() - s_time)))
            if config.SHOW_SCREEN:
                print(f"FPS: {1 / (time.time() - s_time):.2f}", end="\r")
            
    except KeyboardInterrupt:
        if config.PRODUCER_ECHO:
            stop_flag = True
            consumer_thread.join()
        log_message("Exiting...")
        client.disconnect()
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    log_message("Producer exited.")
    
if __name__ == "__main__":
    main()

