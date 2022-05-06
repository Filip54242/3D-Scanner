#import RPi.GPIO as GPIO
import time
import os
import serial


class MotorController:
    def __init__(self):
        self.connection = None
        self.serials_to_try = range(50)
        self.try_to_connect()

    def try_to_connect(self):
        for serial_try in self.serials_to_try:
            if os.path.exists(f'/dev/ttyACM{serial_try}') == True:
                conn = serial.Serial(f'/dev/ttyACM{serial_try}', 115200)
                if conn is not None:
                    self.connection = conn
                    print(f"Connected to : /dev/ttyACM{serial_try}")
                    time.sleep(1)
                    return

    def rotate(self, degrees):

        if type(degrees) is int and \
        self.connection is not None:
            command = f"{str(degrees)}\n"
            self.connection.write(bytes(command.encode("utf-8")))
            self.last_operation=time.time()


motor_con = MotorController()
motor_con.rotate(10)

