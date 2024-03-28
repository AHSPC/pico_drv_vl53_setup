from machine import SoftI2C, Pin, PWM
from time import sleep
from drv8833 import DRV8833  # motor control
from vl53l4cd import VL53L4CD  # distance Sensor

motor_ctl = None
distance_sensor = None


def flash_led():
    print("Flashing Lights! - Challenge 1")
    led = Pin("LED")
    led.on()
    sleep(0.5)
    led.off()


def create_motor_ctl():
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
    return DRV8833(ain1, ain2, bin1, bin2)


def create_distance_sensor():
    print("Confgiure Sensor")
    distance_sensor_i2c = SoftI2C(sda=Pin(0), scl=Pin(1))
    return VL53L4CD(distance_sensor_i2c)


# run some code!
flash_led()
motor_ctl = create_motor_ctl()
distance_sensor = create_distance_sensor()

distance_sensor.start_ranging()
throttle_a_val = 1
throttle_b_val = 1
while True:
    dist = distance_sensor.get_distance()
    print(f"Distance: {dist} cm")
    # if you are too close then reverse the motor
    # - throttle_a_val and throttle_b_val are set from -1 to 1.
    # - negative values reverse the motor.
    # - Think of these as percentages: -0.5 would be 50% power to the motor in reverse
    if dist < ____:
        throttle_a_val = ____
        throttle_b_val = ____
    elif dist < ____:
        throttle_a_val = ____
        throttle_b_val = ____
    ...

    motor_ctl.throttle_a(throttle_a_val)
    motor_ctl.throttle_b(throttle_b_val)
