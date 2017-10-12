import goless
import time
from sys import platform

if platform == "linux" or platform == "linux2":
    import brickpi3


def start_color_sensor(brick, port, channel):
    print("start color sensor")
    setup_sensor(brick, port)
    goless.go(run_color_sensor, brick, port, channel)
    print("color sensor started")


def setup_sensor(brick, port):
    brick.set_sensor_type(port, brick.SENSOR_TYPE.EV3_COLOR_REFLECTED)
    error = True
    while error:
        time.sleep(0.1)
        try:
            brick.get_sensor(port)
            error = False
        except brickpi3.SensorError as error:
            error = True


def run_color_sensor(brick, port, channel):
    # sensor_modes = [(brick.SENSOR_TYPE.EV3_COLOR_REFLECTED, 'reflect'),
    #                 (brick.SENSOR_TYPE.EV3_COLOR_AMBIENT, 'ambiet'),
    #                 (brick.SENSOR_TYPE.EV3_COLOR_COLOR, 'color'),
    #                 (brick.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS, 'color_components')]
    sensor_modes = [(brick.SENSOR_TYPE.EV3_COLOR_COLOR, 'color')]

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
        print("error color", error)
        return error


if __name__ == '__main__':
    print('for local testing read 100 color readings from port 1')
    brick = brickpi3.BrickPi3()
    readings = goless.chan()
    start_color_sensor(brick, brick.PORT_3, readings)

    for i in range(100):
        case, val = goless.select([goless.rcase(readings)])
        print(case, val)

    print('100 reading are done, time to clean and exit')
    brick.reset_all()
