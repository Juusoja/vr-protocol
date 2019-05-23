import struct
import settings

"""
If we're trying to send correct sized packets, the following approximations
are in effect:

Source_id + EOF = 8 bits  --> This is true
Sensor_id + sensor_value = 36 bits --> Each sensor field is 32 bits long
Padding is not taken into account


This means that the size of the packet is quite close to the intended size.

"""

class ProtocolParser:

    def __init__(self):
        self.payload = ''

    """Adds handid to payload. Call right after creating the parser."""
    def init_send(self, hand_id):
        if not settings.send_correct_sized_packets:
            id_in_binary = str(bin(hand_id)[2:])
            jakoj = 4 - (len(id_in_binary) % 4)
            result_string = ""
            i = 0
            while i < jakoj:
                result_string += "0"
                i += 1

            result_string += str(id_in_binary)
            self.payload = result_string
        else:
            # Add 8 bits to the message
            self.payload = "0"
    """Input is int for sensor id and the value."""
    def add_sensor_value(self, sensor_id, value):
        if not settings.send_correct_sized_packets:
            id_in_binary = str(bin(sensor_id)[2:])
            jakoj = 4 - (len(id_in_binary) % 4)
            result_string = ""
            i = 0
            while i < jakoj:
                result_string += "0"
                i += 1
            result_string += str(id_in_binary)
            self.payload += str(result_string)+str(self.int_to_bin(value))
        else:
            # Adds 32 bits to the payload (only the sensor id)
            id_in_binary = str(bin(sensor_id)[2:])
            jakoj = 4 - (len(id_in_binary) % 4)
            result_string = ""
            i = 0
            while i < jakoj:
                result_string += "0"
                i += 1
            result_string += str(id_in_binary)
            self.payload += str(result_string)

    """Call this right before sending to add the end bits and padding."""
    def send(self):
        if not settings.send_correct_sized_packets:
            self.payload += "1111"

            jakoj = 8 - (len(self.payload) % 8)

            i = 0
            while i < jakoj:
                self.payload += "0"
                i += 1
        else:
            # Don't add anything to the message
            pass


        return self.payload

    """Converts integer to simple 32-long string of zeroes and ones."""
    def int_to_bin(self, value):
        #tmp = bin(value)
        #tmp = tmp[2:]
        #jakoj = 32 - (len(tmp) % 32)
        #r = ""
        #i = 0
        #while i < jakoj:
        #    r += "0"
        #    i += 1
        #r += tmp

        return value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')
        
    """Is used to feed data into the object in the receiving side."""
    def parse(self, payload):
        self.payload = payload

    """For printing. Only works if settings.send_correct_sized_packets is False"""
    def __str__(self):
        i = 4
        glove_id = self.payload[0:4]
        r = str("Glove id: {}\n".format(glove_id))

        while self.payload[i:i+4] != b"1111" and i < len(self.payload) - 4:
            r += str("Sensor id: {} - ".format(self.payload[i:i+4]))
            r += str("value: {}\n".format(self.payload[i+4:i+36]))
            i += 36

        return r
