from machine import SoftI2C, Pin, PWM
from time import sleep
from drv8833 import DRV8833 # motor control
from vl53l4cd import VL53L4CD # distance Sensor

print("Flashing Lights! - Does your code run at all!")
led = Pin("LED")
led.on()
sleep(0.5)
led.off()


### Setup DRV8833 (dual motor controller)
# NOTE: feel free to play with the frequency value! The frequency (how many PWM cycles per second
# sent to the DRV pins) changes the behavior of the connected motors, especially at low throttle
# values. After some bried testing, I'd recommend values no lower than 1,000 and no higher than 200,000.
# 40,000 is a good default.
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

# Set both of the drv8833's motors to full throttle
print("Starting motors!")
throttle = 1.0
while throttle > -1.0:
    motor_ctl.throttle_a(throttle)
    motor_ctl.throttle_b(throttle)
    sleep(0.1)
    throttle -= 0.05
    print(throttle)

# Stop both motors after loop exits
print("Stopping motors!")
motor_ctl.stop_a()
motor_ctl.stop_b()

print("Testing Distance Sensor")
# Main loop. Print's the value of `vl53.distance` every time new data is available (matching the sensor's
# clock speed) and simply wait in between measurements. Stops after 100 datapoints have been read.
# Tell the vl53l4cd to start tracking distances

### Setup VL53L4CD (distance sensor)
# NOTE: the fields `inter_measurement` and `timing_budget` can be used for fine tuning!
distance_sensor_i2c = SoftI2C(sda=Pin(0), scl=Pin(1))
distance_sensor = VL53L4CD(distance_sensor_i2c)
distance_sensor.start_ranging()

for _ in range(100):
    # This wait loop can be ommited in order to control main loop timing more precisely (at the cost of
    # receiving the same distance value for multiple cycles)
    while not distance_sensor.data_ready:
        pass
    distance_sensor.clear_interrupt()

    print("Distance: {} cm".format(distance_sensor.distance))

print("Testing Finished - Distance Sensor")
