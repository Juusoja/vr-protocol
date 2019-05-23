"""
Each sensor can have an int value between 0 and 1000.
"""
from protocolparser import ProtocolParser

class Glove:
    def __init__(self, id=1, always_send_all_sensor_data=False):
        self.glove_id = id
        self.always_send_all_sensor_data = always_send_all_sensor_data
        self.current_sensor_values = 5 * [0]
        self.last_sent_sensor_values = 5 * [1000]
        # The difference between old and new value must be greater than this for the value to be sent
        self.send_threshold = 50

    """Adds appropriate sensor values to the given parser."""
    def get_data_to_send(self, parser):
        if self.always_send_all_sensor_data:
            # Send everything
            i = 0
            while i < len(self.current_sensor_values):
                parser.add_sensor_value(i, self.current_sensor_values[i])
                self.last_sent_sensor_values[i] = self.current_sensor_values[i]
                i += 1
        else:
            # Send only that which has changed
            i = 0
            while i < len(self.current_sensor_values):
                if abs(self.current_sensor_values[i] - self.last_sent_sensor_values[i]) > self.send_threshold:
                    parser.add_sensor_value(i, self.current_sensor_values[i])
                    self.last_sent_sensor_values[i] = self.current_sensor_values[i]
                i += 1

    """Simulates a sligth increment to the index finger sensor value (finger bending)."""
    def update_sensor_values(self):
        self.current_sensor_values[1] += 10
        if self.current_sensor_values[1] > 1000:
            self.current_sensor_values[1] = 1000
