# CamJam EduKit 2 - Sensors
# Worksheet 5 - Movement

# Import modules
import RPi.GPIO as G
import time
import datetime

# Set the GPIO naming convention (setmode) and suppress warnings
G.setmode(G.BCM)
G.setwarnings(False)

# Set a variable to hold the Pin identities
PIR_pin = 17
red_led = 18
blue_led = 24
buzzer = 22
LDR_pin = 27

print('PIR Module Test (CTRL-C to exit)')

# Set PIR_pin as input and other pins as output
G.setup(PIR_pin, G.IN)
G.setup(blue_led, G.OUT)
G.setup(red_led, G.OUT)
G.setup(buzzer, G.OUT)

# Create variables to hold previous and current state of PIR input
previous_state = 0
current_state = 0

# Define the function to read the LDR
def Read_LDR():
    LDR_count = 0
    G.setup(LDR_pin, G.OUT)
    G.output(LDR_pin, G.LOW)
    time.sleep(0.1)
    G.setup(LDR_pin, G.IN)
    while (G.input(LDR_pin) == G.LOW):
        LDR_count +=1
        print(LDR_count)
    return LDR_count

# Define functions to light LEDs and sound buzzer
def flash_red():
    for x in range(0,3):
        G.output(red_led, G.HIGH)
        G.output(buzzer, G.HIGH)
        time.sleep(0.5)
        G.output(red_led, G.LOW)
        G.output(blue_led, G.HIGH)
        time.sleep(0.5)
        G.output(blue_led, G.LOW)
        G.output(buzzer, G.LOW)
        time.sleep(0.5)

def steady_blue():
    G.output(blue_led, G.HIGH)
    G.output(red_led, G.LOW)
    G.output(buzzer, G.LOW)

try:
    print('Waiting for PIR to settle...')
    # Loop until PIR output is 0
    print(G.input(PIR_pin))
    while True:# G.input(PIR_pin) ==1:
        current_state = 0

        print('  Ready')
        # Loop until user quites with CTRL-C

        LDR_count = Read_LDR()
        print(LDR_count)
        
        while True:
#           while LDR_count < 2000:
                # Read PIR state
            current_state = G.input(PIR_pin)

            # If the PIR is triggered
            if current_state ==1 and previous_state ==0:
                print('Motion detected at:',datetime.datetime.now().time())
                flash_red()
                # Record previous_state
                previous_state = 1

            # If the PIR has returned to ready state
            elif current_state == 0 and previous_state ==1:
                print('No intruders at:',datetime.datetime.now().time())
                steady_blue()
                previous_state = 0

            # Wait 1/100th of a second
            time.sleep(0.01)

except KeyboardInterrupt:
    print(' Quit')

    # Reset GPIO
    G.cleanup()


 
