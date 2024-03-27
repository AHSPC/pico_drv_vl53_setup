from machine import SoftI2C, Pin, PWM
from time import sleep
from drv8833 import DRV8833
from vl53l4cd import VL53L4CD

led = Pin("LED")
led.on()
sleep(1)
led.off()


### Setup DRV8833 (dual motor controller)
# NOTE: feel free to play with the frequency value! The frequency (how many PWM cycles per second
# sent to the DRV pins) changes the behavior of the connected motors, especially at low throttle
# values. After some bried testing, I'd recommend values no lower than 1,000 and no higher than 200,000.
# 40,000 is a good default.
frequency = 40_000
ain1 = PWM(Pin(15, Pin.OUT), freq=frequency)
ain2 = PWM(Pin(14, Pin.OUT), freq=frequency)
bin1 = PWM(Pin(13, Pin.OUT), freq=frequency)
bin2 = PWM(Pin(12, Pin.OUT), freq=frequency)
drv = DRV8833(ain1, ain2, bin1, bin2)

### Setup VL53L4CD (distance sensor)
# NOTE: the fields `inter_measurement` and `timing_budget` can be used for fine tuning!
vl53_i2c = SoftI2C(sda=Pin(0), scl=Pin(1))
vl53 = VL53L4CD(vl53_i2c)

# Tell the vl53l4cd to start tracking distances
vl53.start_ranging()

# Set both of the drv8833's motors to full throttle
print("Starting motors!")
drv.throttle_a(1.0)
drv.throttle_b(1.0)

# Main loop. Print's the value of `vl53.distance` every time new data is available (matching the sensor's
# clock speed) and simply wait in between measurements. Stops after 100 datapoints have been read.
for _ in range(100):
    # This wait loop can be ommited in order to control main loop timing more precisely (at the cost of
    # receiving the same distance value for multiple cycles)
    while not vl53.data_ready:
        pass
    vl53.clear_interrupt()

    print("Distance: {} cm".format(vl53.distance))

# Stop both motors after loop exits
print("Stopping motors!")
drv.stop_a()
drv.stop_b()
