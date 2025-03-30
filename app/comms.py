
import json
import pickle
import time
import paho.mqtt.client as mqtt

from config import config , log_message

def init_broker() -> mqtt.Client:
    """Initialize the MQTT broker client with the provided configuration."""
    client = mqtt.Client()
    client.username_pw_set(config.BROKER_USER, config.BROKER_PASSWORD)
    return client

def connect_broker(client: mqtt.Client) -> None:
    """Connect to the MQTT broker."""
    client.connect(config.BROKER_IP, config.BROKER_PORT)
    log_message(f"Connected to broker at {config.BROKER_IP}:{config.BROKER_PORT}")

      
landmark_names = [
    "Wrist",                # 0
    "Thumb_CMC",            # 1
    "Thumb_MCP",            # 2
    "Thumb_IP",             # 3
    "Thumb_Tip",            # 4
    "Index_Finger_MCP",     # 5
    "Index_Finger_PIP",     # 6
    "Index_Finger_DIP",     # 7
    "Index_Finger_Tip",     # 8
    "Middle_Finger_MCP",    # 9
    "Middle_Finger_PIP",    # 10
    "Middle_Finger_DIP",    # 11
    "Middle_Finger_Tip",    # 12
    "Ring_Finger_MCP",      # 13
    "Ring_Finger_PIP",      # 14
    "Ring_Finger_DIP",      # 15
    "Ring_Finger_Tip",      # 16
    "Pinky_MCP",            # 17
    "Pinky_PIP",            # 18
    "Pinky_DIP",            # 19
    "Pinky_Tip"             # 20
]

class Hands_Information:
    def __init__(self):
        self.timestamp = time.time()

    def add_hand(self, hand, handedness, pointing_angle):
        hand_prefix = "hand" + handedness[0].upper()
        self.add_hand_info(hand, hand_prefix, pointing_angle)
        
    def add_hand_info(self, hand, hand_prefix, pointing_angle):
        self.add_pointing_angle(hand_prefix, pointing_angle)
        self.__dict__[hand_prefix + "_has"] = True
        for ind , name in enumerate(landmark_names):
            landmark = hand.landmark[ind]
            if landmark is not None:
                self.add_landmark(hand_prefix, name , landmark)
            
    def add_pointing_angle(self, hand_prefix, pointing_angle):
        self.__dict__[hand_prefix + "_direction"] = pointing_angle
        
    def add_landmark(self, hand_prefix, name, landmark):
        self.__dict__[hand_prefix + "_" + name + "_x"] = landmark.x
        self.__dict__[hand_prefix + "_" + name  + "_y"] = landmark.y
        
    def to_flat_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
    
    def to_json(self):
        return json.dumps(self.to_flat_dict())
    
    def from_json(self, json_str):
        self.__dict__ = json.loads(json_str)
        return self
        
    def to_pickle(self):
        return pickle.dumps(self.to_flat_dict())
    
    def from_pickle(self, pickle_str):
        self.__dict__ = pickle.loads(pickle_str)
        return self
        
    def __str__(self):
        return str(self.to_flat_dict())