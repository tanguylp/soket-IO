# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from digi.xbee.devices import XBeeDevice, XBee64BitAddress, RemoteXBeeDevice
from digi.xbee.io import IOLine, IOMode, IOValue, IOSample
from digi.xbee.models.status import ModemStatus
import time
import threading
import socket

# TODO: Replace with the serial port where your local module is connected to. 
PORT = "/dev/ttyUSB0"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

REMOTE_NODE_ID = "0013A2004152EED9"

IOLINE_OUT1 = IOLine.DIO4_AD4
IOLINE_OUT2 = IOLine.DIO1_AD1
IOLINE_Wake = IOLine.DIO8


def main():

    print(" +-----------------------------------------------+")
    print(" | XBee Python Library Get/Set Remote DIO Sample |")
    print(" +-----------------------------------------------+\n")

    host = "192.168.16.1"
    port = 5000

    mySocket = socket.socket()
    mySocket.bind((host,port))

    stop = False
    th = None

    local_device = XBeeDevice(PORT, BAUD_RATE)

    try:
        local_device.open()

        # Obtain the remote XBee device from the XBee network.
        xbee_network = local_device.get_network()
        remote_device = RemoteXBeeDevice(local_device, XBee64BitAddress.from_hex_string(REMOTE_NODE_ID))
        print(remote_device)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        def HighLow():
            remote_device.set_dio_value(IOLINE_OUT1,IOValue.HIGH)
            remote_device.set_dio_value(IOLINE_OUT2,IOValue.LOW)

            value_OUT2 = remote_device.get_dio_value(IOLINE_OUT2)
            value_OUT1 = remote_device.get_dio_value(IOLINE_OUT1)
            print(value_OUT2)
            print(value_OUT1)
            time.sleep(0.4)

        def LowHigh():
            remote_device.set_dio_value(IOLINE_OUT1,IOValue.LOW)
            remote_device.set_dio_value(IOLINE_OUT2,IOValue.HIGH)

            value_OUT2 = remote_device.get_dio_value(IOLINE_OUT2)
            value_OUT1 = remote_device.get_dio_value(IOLINE_OUT1)
            print(value_OUT2)
            print(value_OUT1)
            time.sleep(0.4)

        def off():
            remote_device.set_dio_value(IOLINE_OUT1,IOValue.LOW)
            remote_device.set_dio_value(IOLINE_OUT2,IOValue.LOW)

        mySocket.listen(1)
        conn, addr = mySocket.accept()
        print ("Connection from: " + str(addr))
        exit = ''
        while exit != 'OFF':
            data = conn.recv(1024).decode()
            if not data:
                    break
            print ("from connected  user: " + str(data))
             
            data = str(data).upper()
            print ("sending: " + str(data))
            conn.send(data.encode())
            if str(data) == 'OPEN':
                LowHigh()
                off()
            elif str(data) == 'CLOSE':
                HighLow()
                off()

            elif str(data) == 'OFF':
                exit = data

        conn.close()
        
    finally:
        stop = True
        if th is not None and th.is_alive():
            th.join()
        if local_device is not None and local_device.is_open():
            local_device.close()


if __name__ == '__main__':
    main()
