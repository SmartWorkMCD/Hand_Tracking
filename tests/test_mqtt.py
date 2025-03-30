import pytest
from unittest.mock import patch, MagicMock
import paho.mqtt.client as mqtt
from app.comms import init_broker, connect_broker  # Import the functions from your script

@pytest.fixture(autouse=True)
def mock_config():
    """Mock configuration settings."""
    with patch('app.config.config') as mock:
        mock.BROKER_USER = "admin"
        mock.BROKER_PASSWORD = "password"
        mock.BROKER_IP = "127.0.0.1"
        mock.BROKER_PORT = 1883
        yield mock

def test_init_broker(mock_config):
    """Test the initialization of the MQTT broker client."""
    # Mock the mqtt.Client class
    with patch('paho.mqtt.client.Client') as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client  # Make init_broker return the mock client

        # Initialize broker
        client = init_broker()

        # Check if the client is a MagicMock instance (since it's mocked)
        assert isinstance(client, MagicMock)

        # Check if the username_pw_set method was called with the correct parameters
        client.username_pw_set.assert_called_with("admin", "admin")

def test_connect_broker(mock_config):
    """Test the connection to the broker."""
    # Mock the mqtt.Client class used in connect_broker
    with patch('paho.mqtt.client.Client') as mock_mqtt_client:
        client = MagicMock()
        mock_mqtt_client.return_value = client  # Make connect_broker use the mock client

        # Call the connect function
        connect_broker(client)

        # Check if connect was called with the correct arguments
        client.connect.assert_called_once_with("127.0.0.1", 1883)
