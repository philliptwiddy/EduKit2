#CamJam Edukit 2 - Sensors
# Worksheet 3 - Temperature

# Import libraries
import os
import glob
import time
import RPi.GPIO as G

# Initialise the GPIO Pins
os.system('modprobe w1-gpio') # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

# Set GPIO numbering mde
G.setmode(G.BCM)

# Store Pin numbers in variables
red_led = 18
blue_led = 24
buzzer = 22

# Setup the GPIO Pins for the LEDs and buzzer
G.setup(red_led, G.OUT)
G.setup(blue_led, G.OUT)
G.setup(buzzer, G.OUT)

# Finds the correct devce file that holds the temperature data
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# A function to light the leds / sound the buzzer
def led_off():
    G.output(red_led, G.LOW)
    G.output(blue_led, G.LOW)
    G.output(buzzer, G.LOW) # buzzer will always be off when it's cold

def blue_led_on():
    G.output(red_led, G.LOW)
    G.output(blue_led, G.HIGH)
    G.output(buzzer, G.LOW) # buzzer will always be off when it's cold

def red_led_on(): # buzzer not set using this as it could be on or off when it's hot
    G.output(red_led, G.HIGH)
    G.output(blue_led, G.LOW)

def buzzer_on():
    G.output(buzzer, G.HIGH)

def buzzer_off():
    G.output(buzzer, G.LOW)

# A function that reads the sensor data
def read_temp_raw():
    f = open(device_file, 'r') # Opens the temperature device file
    lines = f.readlines() # Returns the text
    f.close()
    return lines

# Convert the value of the sensor into a temperature
def read_temp():
    lines = read_temp_raw() # Read the temperature 'device file'

    # While the first line does not contain 'YES', wait for 0.2s
    # and then read the device file again.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    # Look for the position of the '=' in the second line of the
    # device file.
    equals_pos = lines[1].find('t=')

    # If the '=' is found, convert the rest of the line after the
    # '=' into degrees Celsius, then degrees Fahrenheit
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c *9.0 /5.0 +32.0
        return temp_c, temp_f

# Print out the temperature until the programe is stopped.
while True:
    temp_c, temp_f = read_temp()
    if temp_c < 20:
        blue_led_on()
    elif temp_c >= 20 and temp_c <30:
        led_off()
    elif temp_c >= 30 and temp_c <35:
        red_led_on()
        buzzer_off()
    else:
        red_led_on()
        buzzer_on()
    print(read_temp())
    time.sleep(1)
