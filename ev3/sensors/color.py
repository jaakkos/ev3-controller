import goless
import time
from sys import platform
if platform == "linux" or platform == "linux2":
  import brickpi3

def start_color_sensor(brick, port, channel):
  print("start color sensor")
  goless.go(run_color_sensor, brick, port, channel)
  print("color sensor started")

def run_color_sensor(brick, port, channel):
  sensor_modes = [(brick.SENSOR_TYPE.EV3_COLOR_REFLECTED, 'reflect'), 
                  (brick.SENSOR_TYPE.EV3_COLOR_AMBIENT, 'ambiet'), 
                  (brick.SENSOR_TYPE.EV3_COLOR_COLOR, 'color'), 
                  (brick.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS, 'color_coponents')]

  while True:
    for sensor_mode in sensor_modes:
      sensor_value = read_sensor(brick, port, sensor_mode[0])
      if sensor_value:
        channel.send(('color', (sensor_mode[1], sensor_value)))
      time.sleep(0.02)
    
    sleep(0.1)

def read_sensor(brick, port, sensor_type):
  try:
    brick.set_sensor_type(port, sensor_type)
    time.sleep(0.02)
    return brick.get_sensor(port)
  except brickpi3.SensorError as error:
    print(error)

if __name__ == '__main__':
  print('for local testing read 100 color readings from port 1')
  brick = brickpi3.BrickPi3()
  readings = goless.chan()

  print('start color sensor')
  start_color_sensor(brick, brick.PORT_3, readings)

  for i in range(100):
    case, val = goless.select([goless.rcase(readings)])
    print(val)

  print('100 reading are done, time to clean and exit')
  brick.reset_all()
  
