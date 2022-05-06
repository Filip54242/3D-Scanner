import sys
from machine import Pin
from time import sleep

pins = [Pin(21,Pin.OUT),
        Pin(19,Pin.OUT),
        Pin(20,Pin.OUT),
        Pin(18,Pin.OUT)]

step_count=11632
step_sleep=0.01
steps_per_angle=step_count/360
step_sequence=[
              [1, 0, 1, 0],
              [0, 1, 1, 0],
              [0, 1, 0, 1],
              [1, 0, 0, 1]]
step_sequence_reset=len(step_sequence)

def handle_sequence(steps,sequence):
         for step in range(0,steps):
             for pin_index in range(len(pins)):
                 pins[pin_index].value(step_sequence[step%step_sequence_reset][pin_index])
             
             sleep(step_sleep)


def rotate_clockwise(angle):
        if angle>0:
            steps=int(steps_per_angle*angle)
            handle_sequence(steps,step_sequence)

def rotate_counter_clockwise(angle):
        if angle>0:
            steps=int(steps_per_angle*angle)
            handle_sequence(steps,step_sequence[::-1])
  
def rotate(degrees):
        if degrees>0:
            rotate_clockwise(degrees)
        else:
            rotate_counter_clockwise(-degrees)

while True:
    data = sys.stdin.readline()
    angle = int(data)
    rotate(angle)