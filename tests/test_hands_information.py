import pytest
import time
from unittest.mock import MagicMock
from app.comms import Hands_Information, landmark_names  # Import the class and necessary objects

@pytest.fixture
def mock_hand():
    """Mock a hand object."""
    hand = MagicMock()
    hand.landmark = [MagicMock(x=i, y=i+1) for i in range(21)]  # Create 21 landmarks for the hand
    return hand

def test_add_hand(mock_hand):
    """Test adding a hand to the Hands_Information."""
    hands_info = Hands_Information()
    hands_info.add_hand(mock_hand, "Left", 45)
    
    # Check if landmarks were added correctly
    for i, name in enumerate(landmark_names):
        assert hasattr(hands_info, f"handL_{name}_x")
        assert hasattr(hands_info, f"handL_{name}_y")
        assert getattr(hands_info, f"handL_{name}_x") == i
        assert getattr(hands_info, f"handL_{name}_y") == i + 1
    
    # Check if pointing angle was added
    assert hasattr(hands_info, "handL_direction")
    assert hands_info.handL_direction == 45

def test_to_json(mock_hand):
    """Test the to_json method."""
    hands_info = Hands_Information()
    hands_info.add_hand(mock_hand, "Right", 30)
    
    json_data = hands_info.to_json()
    
    # Test if the returned JSON is a string and contains relevant fields
    assert isinstance(json_data, str)
    assert '"handR_direction": 30' in json_data
    assert '"handR_Wrist_x": 0' in json_data

def test_from_json(mock_hand):
    """Test the from_json method."""
    hands_info = Hands_Information()
    hands_info.add_hand(mock_hand, "Left", 45)
    
    json_data = hands_info.to_json()
    new_hands_info = Hands_Information().from_json(json_data)
    
    # Check if the data is correctly deserialized
    assert hasattr(new_hands_info, "handL_Wrist_x")
    assert new_hands_info.handL_Wrist_x == 0

def test_to_pickle(mock_hand):
    """Test the to_pickle method."""
    hands_info = Hands_Information()
    hands_info.add_hand(mock_hand, "Left", 45)
    
    pickle_data = hands_info.to_pickle()
    
    # Test if the returned data is a byte object
    assert isinstance(pickle_data, bytes)

def test_from_pickle(mock_hand):
    """Test the from_pickle method."""
    hands_info = Hands_Information()
    hands_info.add_hand(mock_hand, "Left", 45)
    
    pickle_data = hands_info.to_pickle()
    new_hands_info = Hands_Information().from_pickle(pickle_data)
    
    # Check if the data is correctly deserialized
    assert hasattr(new_hands_info, "handL_Wrist_x")
    assert new_hands_info.handL_Wrist_x == 0
