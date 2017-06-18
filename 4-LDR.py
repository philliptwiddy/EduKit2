# CamJam EduKit 2 - Sensors
# Worksheet 4 - Light

# Import libraries
import time
import RPi.GPIO as G

# Set the GPIO naming convention (setmode) and setwarnings
G.setmode(G.BCM)
G.setwarnings(False)

# Set variable for the Pin numbers
ldr_pin = 27 # Light-Dependent Resistor (LDR)
led_red = 18 # red LED
led_blue = 24 # blue LED
buzzer = 22 # buzzer

# Setup the LEDs and buzzer pins
G.setup(led_red, G.OUT)
G.setup(led_blue, G.OUT)
G.setup(buzzer, G.OUT)

def dull(): # Turn on blue LED, turn off red LED and buzzer 
    G.output(led_red, G.LOW)
    G.output(led_blue, G.HIGH)
    G.output(buzzer, G.LOW)

def bright(): # Turn on red LED, turn off blue LED and buzzer 
    G.output(led_red, G.HIGH)
    G.output(led_blue, G.LOW)
    G.output(buzzer, G.LOW)

def very_bright(): # Turn on red LED and buzzer, turn off blue LED
    G.output(led_red, G.HIGH)
    G.output(led_blue, G.LOW)
    G.output(buzzer, G.HIGH)

def ReadLDR():
    LDRCount = 0 # Sets the count to 0
    G.setup(ldr_pin, G.OUT) # Sets the LDR pin to output
    G.output(ldr_pin, G.LOW) # Sets output to LOW (Ov), so capacitor v is higher
    time.sleep(0.1) # 0.1s is sufficient for the capacitor to discharge
    G.setup(ldr_pin, G.IN) # Now sets LDR pin to be input, able to read what is happening
    # While the input pin reads 'off' or LOW, count
    while (G.input(ldr_pin) == G.LOW):
        LDRCount += 1 # Add one to the counter
    return LDRCount

while True:
    lux = ReadLDR()
    if lux > 2000:
        dull()
    elif lux > 900 and lux <=2000:
        bright()
    else:
        very_bright()
    print(ReadLDR())
    time.sleep(1) # Wait for a second
