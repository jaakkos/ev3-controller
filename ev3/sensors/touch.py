import goless
import time
from sys import platform

if platform == "linux" or platform == "linux2":
    import brickpi3


def start_touch_sensor(brick, port, channel):
    print("start touch sensor")
    setup_sensor(brick, port)
    goless.go(run_touch_sensor, brick, port, channel)
    print("touch sensor started")


def setup_sensor(brick, port):
    brick.set_sensor_type(port, brick.SENSOR_TYPE.TOUCH)
    error = True
    while error:
        time.sleep(0.1)
        try:
            brick.get_sensor(port)
            error = False
        except brickpi3.SensorError as error:
            error = True


def run_touch_sensor(brick, port, channel):
    while True:
        try:
            sensor_value = brick.get_sensor(port)
            time.sleep(0.5)
            channel.send(sensor_value)
        except brickpi3.SensorError as error:
            print("error touch", error)
            return None


if __name__ == '__main__':
    print('for local testing read 100 touch readings from port 1')
    brick = brickpi3.BrickPi3()
    readings = goless.chan()

    print('start touch sensor')
    start_touch_sensor(brick, brick.PORT_1, readings)

    for i in range(100):
        case, val = goless.select([goless.rcase(readings)])
        print(case, val)

    print('100 reading are done, time to clean and exit')
    brick.reset_all()
