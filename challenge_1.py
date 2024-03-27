from machine import SoftI2C, Pin, PWM
from time import sleep
from drv8833 import DRV8833  # motor control
from vl53l4cd import VL53L4CD  # distance Sensor


def flash_led():
    print("Flashing Lights! - Challenge 1")
    led = Pin("LED")
    led.on()
    sleep(0.5)
    led.off()


def create_motor_ctl():
    print("Confgiure Motor")
    frequency = 100000
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
motor_ctl.throttle_a(1)
distance_sensor.start_ranging()
while True:
    print("Distance: {} cm".format(distance_sensor.distance))
    distance_sensor.clear_interrupt()
    if distance_sensor.distance > 50:
        motor_ctl.throttle_a(1)
    elif distance_sensor.distance < 50:
        motor_ctl.throttle_a(0.5)
    elif distance_sensor.distance < 10:
        motor_ctl.stop_a()
