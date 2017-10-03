from gevent import monkey
monkey.patch_all()

import goless
import time
from flask_socketio import SocketIO, emit, send
from sys import platform
from sensors import start_color_sensor, start_infrared_sensor, start_touch_sensor

if platform == "linux" or platform == "linux2":
  import brickpi3
  
def start():
  if platform == "linux" or platform == "linux2":
    socketio = SocketIO(message_queue='redis://')
    start_sensors(socketio)
  else: 
    print("not working")

def start_sensors(socketio):
  print("Start sensors")
  brick = brickpi3.BrickPi3()
  color_readings = goless.chan()
  infrared_readings = goless.chan()
  touch_readings = goless.chan()
  start_touch_sensor(brick, brick.PORT_1, touch_readings)
  start_color_sensor(brick, brick.PORT_2, color_readings)
  start_infrared_sensor(brick, brick.PORT_3, infrared_readings)

  while True:

    value = color_readings.recv()
    message_type = 'color-' + value[0]
    message_data = {'data': value[1]}
    socketio.emit(message_type, message_data)

    print("received", message_type, message_data)

    value = infrared_readings.recv()
    message_type = 'infrared-' + value[0]
    message_data = {'data': value[1]}
    socketio.emit(message_type, message_data)

    print("received", message_type, message_data)

    value = touch_readings.recv()
    message_type = 'touch'
    message_data = {'data': value}
    socketio.emit(message_type, message_data)

    print("received", message_type, message_data)

    time.sleep(0.2)
    

if __name__ == '__main__':
  start()
  