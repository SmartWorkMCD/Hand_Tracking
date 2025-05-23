from dataclasses import dataclass, fields
import os
import time
from dotenv import load_dotenv
load_dotenv(override=True)

def log_message(message: str, *args, level: str = "INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not config.VERBOSE:
        if level != "INFO":
            print(f"{timestamp} [{level}] {message}", *args)
        return 
    
    print(f"{timestamp} [{level}] {message}", *args)

class IPAddress(str):
    def __new__(cls, value: str):
        if not cls.is_valid(value):
            raise ValueError(f"Invalid IP address: {value}")
        return str.__new__(cls, value)

    @staticmethod
    def is_valid(ip: str) -> bool:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not (0 <= int(part) <= 255):
                return False
        return True

@dataclass
class Config:
    FLIP_CAMERA_V: bool = False
    FLIP_CAMERA_H: bool = True
    SHOW_SCREEN: bool = False
    TARGET_FPS: int = 60
    CAMERA_ID: int = 0

    BROKER_IP: str = os.environ.get("BROKER_IP", "mqtt-broker")
    BROKER_PORT: int = int(os.environ.get("BROKER_PORT", 1883))
    BROKER_USER: str = os.environ.get("BROKER_USER", "user")
    BROKER_PASSWORD: str = os.environ.get("BROKER_PASSWORD", "password")
    BROKER_TOPIC: str = "hands/position"
    
    VERBOSE: bool = False
    PRODUCER_ECHO: bool = False

def string_to_bool(s: str) -> bool:
    s = s.strip().lower() 
    if s in ["true", "1"]:
        return True
    elif s in ["false", "0"]:
        return False
    else:
        raise ValueError(f"Cannot convert '{s}' to boolean. Expected 'true' or 'false'.")

def init_config():
    config = Config()
    for field in fields(Config):
        value = os.getenv(field.name)
        if value:
            try:
                if field.type == bool:
                    value = string_to_bool(value)
                else:
                    value = field.type(value)
                setattr(config, field.name, value)
            except Exception as e:
                raise ValueError(f"Error setting {field.name} to {value}: {e}")
    return config
    
def validate_config(config: Config):
    for field in fields(config):
        value = getattr(config, field.name)
        expected_type = field.type
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Config value {field.name} must be of type {expected_type}, but got {type(value)}"
            )
    return config
    
    
config = validate_config(init_config())
def refresh_config():
    global config
    config = validate_config(init_config())
    return config
log_message(config, level="DEBUG")