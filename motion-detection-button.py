
import os
import pygame
import time
import csv

from pathlib import Path

from datetime import datetime

from gpiozero import LED, Buzzer, MotionSensor, Button

from signal import pause
#we will create an instance of the LED method from the gpio import and give it pin number 15 or input and output
led = LED(14)

#pin 15 will be used to send a signal to the buzzer to sound
buzzer = Buzzer(15)

#pin 4 wiill be used to pick up on any motion detected from the PIR sensor
motion_sensor = MotionSensor(18)

#pin 21 will be responsible for taking "input" (user pressing button) and starting the motion detection process
button = Button(20)

#we will then define the path where we intend to store the csv file we will later write to, since its in the same diectory we only include its title
output_csv_path = Path("detected_motion.csv")

#now we establish a dictionary with two keys, the start and end of the motion detection
motion = {
    "start_time" : None,
    "end_time" : None}


def write_to_csv():
#we will then check if this is a new file being created or if its already a created file, depending on this we may or mayy not include a header row
    first_write = not output_csv_path.is_file()
#we will then open the csv file with the path variable with the append mide active    
    with open(output_csv_path, "a") as file:
#we will then establish the header column names by assigning them too the keys of the moton dictiionary 
        field_names = motion.keys()
        
        writer = csv.DictWriter(file, field_names)
#we will then test if its the intial write to this file, if so we will write a header to categorise our rows        
        if first_write:
            writer.writeheader()
#regardless we intend to add a new row with both the start and end time of all detections
        writer.writerow(motion)
    

def intruder_alert():
    """the purpose of this function is to initiliase a method for dealing with sound files
    we will then use the method to load the specific sound file then play it """
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Desktop/physical-programming/progs/alarm.wav")
    pygame.mixer.music.play()


def start_motion():
    """this function will be invoked from the main loop and will be responsible for timestamping the time of motion detection"""
    """we will also use this to light the led when motion is sensed and also to sound the buzzer"""
    
    led.blink(0.5, 0.5)
    
    buzzer.beep(0.5, 0.5)
    
    motion["start_time"] = datetime.now()
    
    intruder_alert()
    os.system('fswebcam --no-banner /home/pi/Desktop/physical-programming/progs-for-develop/%H%M%S.jpg')
    
    
    print("motion detected")

def end_motion():
    
    if motion["start_time"]:
        led.off()
        buzzer.off()
        motion["end_time"] = datetime.now()
        
        write_to_csv()
        
        motion["start_time"] =None
        
        motion["end_time"] = None
        
    print("motion ended")








button.wait_for_press()

if button.is_pressed:
    print("Readying Sensor")
    #we will wait till there is no motion at all before beginnig recording
    motion_sensor.wait_for_no_motion()

    print("Sensor Ready")
    #the following shows two functions being assigned to methods on the motion sensor, this shows we can easily pass functionalityy of the device over to functons to handle
    #now we will assign the functiion for marking the intial timestamp to the sensors motion detection function
    motion_sensor.when_motion = start_motion
    #we also use the motion sensors built in method to detect no motiion and set it equal to the end motion fucntion

    motion_sensor.when_no_motion = end_motion

    pause()

            
