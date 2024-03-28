from machine import SoftI2C, Pin, PWM
from time import sleep
from drv8833 import DRV8833 # motor control
from vl53l4cd import VL53L4CD # distance Sensor

motor_ctl = None
distance_sensor = None

def flash_led():
    print("Flashing Lights! - Challenge 1")
    led = Pin("LED")
    led.on()
    sleep(0.5)
    led.off()

def configure_motor_ctl():
    global motor_ctl
    print("Confgiure Motor")
    frequency = 40000
    ain1 = PWM(Pin(15, Pin.OUT))
    ain2 = PWM(Pin(14, Pin.OUT))
    bin1 = PWM(Pin(13, Pin.OUT))
    bin2 = PWM(Pin(12, Pin.OUT))

    ain1.freq(frequency)
    ain2.freq(frequency)
    bin1.freq(frequency)
    bin2.freq(frequency)
    motor_ctl = DRV8833(ain1, ain2, bin1, bin2)

def configure_distance_sensor():
    global distance_sensor
    print("Confgiure Sensor")
    distance_sensor_i2c = SoftI2C(sda=Pin(0), scl=Pin(1))
    distance_sensor = VL53L4CD(distance_sensor_i2c)

# run some code!
flash_led()
configure_motor_ctl()
configure_distance_sensor()
throttle_a_val = 1
throttle_b_val = 1

distance_sensor.start_ranging()
while True:
    print("Distance: {} cm".format(distance_sensor.distance))
    # if you are too close then reverse the motor
    # - throttle_a_val and throttle_b_val are set from -1 to 1.
    # - negative values reverse the motor. 
    # - Think of these as percentages: -0.5 would be 50% power to the motor in reverse
    if distance_sensor.distance < _____:
        throttle_a_val = _____ 
        throttle_b_val = _____ 
    elif distance_sensor.distance < _____:
        throttle_a_val = _____ 
        throttle_b_val = _____ 
    ...
    
    motor_ctl.throttle_a(throttle_a_val)
    motor_ctl.throttle_b(throttle_b_val)

