import goless
import time
from sys import platform

if platform == "linux" or platform == "linux2":
    import brickpi3


def start_infrared_sensor(brick, port, channel):
    print("start infrared sensor")
    setup_sensor(brick, port)
    goless.go(run_infrared_sensor, brick, port, channel)
    print("infrared sensor started")


def setup_sensor(brick, port):
    brick.set_sensor_type(port, brick.SENSOR_TYPE.EV3_INFRARED_PROXIMITY)
    error = True
    while error:
        time.sleep(0.1)
        try:
            brick.get_sensor(port)
            error = False
        except brickpi3.SensorError as error:
            error = True


def run_infrared_sensor(brick, port, channel):
    sensor_modes = [(brick.SENSOR_TYPE.EV3_INFRARED_PROXIMITY, 'proximity'),
                    (brick.SENSOR_TYPE.EV3_INFRARED_REMOTE, 'remote'),
                    (brick.SENSOR_TYPE.EV3_INFRARED_SEEK, 'seek')]

    while True:
        for sensor_mode in sensor_modes:
            time.sleep(0.01)
            sensor_value = read_sensor(brick, port, sensor_mode[0])
            if sensor_value:
                channel.send((sensor_mode[1], sensor_value))
                if isinstance(sensor_value, brickpi3.SensorError):
                    break


def read_sensor(brick, port, sensor_type):
    try:
        brick.set_sensor_type(port, sensor_type)
        time.sleep(0.01)
        return brick.get_sensor(port)
    except brickpi3.SensorError as error:
        print("error infrared", error)
        return error


if __name__ == '__main__':
    print('for local testing read 100 infrared readings from port 1')
    brick = brickpi3.BrickPi3()
    readings = goless.chan()

    print('start infrared sensor')
    start_infrared_sensor(brick, brick.PORT_2, readings)

    for i in range(100):
        case, val = goless.select([goless.rcase(readings)])
        print(case, val)

    print('100 reading are done, time to clean and exit')
    brick.reset_all()
