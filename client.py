"""
A simple Python script to send messages to a sever over Bluetooth using
Python sockets (with Python 3.3 or above).
"""



import socket
import settings
from protocolparser import ProtocolParser

serverMACAddress = settings.MAC_Ilpo
port = 3
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((serverMACAddress,port))

parser = ProtocolParser()
parser.init_send(2)
parser.add_sensor_value(2, 20)
parser.add_sensor_value(1, 400)
parser.send()

s.send(bytes(parser.payload, "UTF-8"))
"""
while 1:
    text = input()
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
"""
print("Done. Ending connection...")
s.close()
