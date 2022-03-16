import RPi.GPIO as GPIO
from time import sleep

class MotorController:
    def __init__(self):
        self.stepper_pins=[23,25,24,8]
        self.step_sleep=0.002
        self.step_count=11632
        self.steps_per_angle=self.step_count/360
        self.clockwise_rotation=False
        self.step_sequence=[
            [GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
            [GPIO.LOW,GPIO.HIGH,GPIO.HIGH,GPIO.LOW],
            [GPIO.LOW,GPIO.HIGH,GPIO.LOW,GPIO.HIGH],
            [GPIO.HIGH,GPIO.LOW,GPIO.LOW,GPIO.HIGH]]
        self.step_sequence_reset=len(self.step_sequence)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.stepper_pins,GPIO.OUT)

    def __del__(self):
        self.clear()

    def clear(self):
        #GPIO.output( self.stepper_pins, GPIO.LOW )
        GPIO.cleanup()
    
    def handle_sequence(self,steps,sequence):
        for step in range(0,steps):
            GPIO.output(self.stepper_pins,sequence[step%self.step_sequence_reset])
            sleep(self.step_sleep)
    
    def rotate_clockwise(self,angle):
        if angle>0:
            steps=int(self.steps_per_angle*angle)
            self.handle_sequence(steps,self.step_sequence)

    def rotate_counter_clockwise(self,angle):
        if angle>0:
            steps=int(self.steps_per_angle*angle)
            self.handle_sequence(steps,self.step_sequence[::-1])
    
    def rotate(self,degrees):
        if degrees>0:
            self.rotate_clockwise(degrees)
        else:
            self.rotate_counter_clockwise(-degrees)



if __name__=='__main__':
    motor=MotorController()
    motor.rotate(-50)