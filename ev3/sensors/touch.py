import goless
import time
from sys import platform
if platform == "linux" or platform == "linux2":
  import brickpi3

def start_touch_sensor(brick, port, channel):
  print("start touch sensor")
  goless.go(run_touch_sensor, brick, port, channel)
  print("touch sensor started")

def run_touch_sensor(brick, port, channel):
  brick.set_sensor_type(port, brick.SENSOR_TYPE.TOUCH)
  time.sleep(0.1)

  while True:
    try:
      sensor_value = brick.get_sensor(port)
      print(sensor_value)
      if sensor_value:
        channel.send(('touch', sensor_value))

    except brickpi3.SensorError as error:
      print(error)

    print("looop")
    time.sleep(0.02)

if __name__ == '__main__':
  print('for local testing read 100 touch readings from port 1')
  brick = brickpi3.BrickPi3()
  readings = goless.chan()

  print('start touch sensor')
  start_touch_sensor(brick, brick.PORT_1, readings)

  for i in range(100):
    case, val = goless.select([goless.rcase(readings)])
    print(val)

  print('100 reading are done, time to clean and exit')
  brick.reset_all()

