"""
A simple Python script to send messages to a sever over Bluetooth using
Python sockets (with Python 3.3 or above).
"""

import socket
import settings
from protocolparser import ProtocolParser
from glove import Glove
from datetime import datetime


test_time = 1000/(10 * settings.polling_rate) * 1000000 # Microseconds

# Open up the connection
serverMACAddress = settings.MAC_Juuso
port = 3
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))

# Make a virtual glove and parser
glove = Glove(always_send_all_sensor_data=settings.glove_sends_all_data)
parser = ProtocolParser()
parser.init_send(2)

start_time = datetime.now()
last_poll_time = datetime.now()
last_movement_time = datetime.now()

hz_in_microsecs = 1/(settings.polling_rate * 1000 * 1000)
test_ticks = 10000 # The amount of times our finger changes physical positions

# Run loop for the duration of the test
while (last_poll_time - start_time).microseconds < test_time:
    # Increment finger position if needed
    if (datetime.now() - last_movement_time).microseconds > test_time/test_ticks:
        glove.update_sensor_values()
        last_movement_time = datetime.now()

    # Check that we are sending in accordance to the polling rate
    if (datetime.now() - last_poll_time).microseconds > hz_in_microsecs:
        # Insert appropriate sensor values to the parser
        parser = glove.get_data_to_send(parser)
        # Insert end-of-message and padding bits
        parser.send()
        # Cram the data to the socket
        s.send(bytes(parser.payload, "UTF-8"))
        # Update time
        last_poll_time = datetime.now()

print("Done. Ending connection...")
s.close()
