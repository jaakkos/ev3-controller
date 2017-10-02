import goless
import time
import start_color_sensor, start_infrared_sensor, start_touch_sensor from sensors
if platform == "linux" or platform == "linux2":
  import brickpi3
  
def start(emit):
  if platform == "linux" or platform == "linux2":
    start_sensors(emit)
  else: 
    print("not working")

def start_sensors():
  brick = brickpi3.BrickPi3()
  color_readings = goless.chan()
  infrared_readings = goless.chan()
  touch_readings = goless.chan()

  start_touch_sensor(brick, brick.PORT_1, touch_readings)
  start_color_sensor(brick, brick.PORT_2, color_readings)
  start_infrared_sensor(brick, brick.PORT_3, infrared_readings)

  goless.go(start_sensors, emit, color_readings, infrared_readings, touch_readings)


def start_emitter(emit, color_readings, infrared_readings, touch_readings):
  case, val = goless.select([goless.rcase(color_readings),
                             goless.rcase(infrared_readings)
                             goless.rcase(touch_readings)])
  emit(val[0], {'data': val[1]}, broadcast=True)
  