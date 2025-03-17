from dataclasses import dataclass, fields
import os
from typing import Optional

@dataclass
class Config:
    FLIP_CAMERA_V: bool = False
    FLIP_CAMERA_H: bool = True
    SHOW_SCREEN: bool = True
    TARGET_FPS: int = 60
    VERBOSE: bool = False

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
print(config)