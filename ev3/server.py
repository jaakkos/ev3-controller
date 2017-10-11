#!/usr/bin/env python
import goless
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from sys import platform
from threading import Lock

from sensors import start_color_sensor, start_infrared_sensor, start_touch_sensor

if platform == 'linux' or platform == 'linux2':
    import brickpi3
else:
    print('Fatal error')
    quit()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)
touch_sensor_thread = None
color_sensor_thread = None
infrared_sensor_thread = None
thread_lock = Lock()
brick = brickpi3.BrickPi3()

sensor_ports = [brick.PORT_1, brick.PORT_2, brick.PORT_3, brick.PORT_4]
motor_ports = [brick.PORT_A, brick.PORT_B, brick.PORT_C, brick.PORT_D]
ports = {
    1: brick.PORT_1,
    2: brick.PORT_2,
    3: brick.PORT_3,
    4: brick.PORT_4,
    'A': brick.PORT_A,
    'B': brick.PORT_B,
    'C': brick.PORT_C,
    'D': brick.PORT_D
}


def read_touch_sensor(port):
    touch_readings = goless.chan()
    start_touch_sensor(brick, port, touch_readings)
    while True:
        value = touch_readings.recv()
        message_type = 'touch'
        message_data = {'data': value}
        socketio.emit(message_type, message_data)
        print('emitted', message_type, message_data)
        socketio.sleep(0.2)


def read_color_sensor(port):
    color_readings = goless.chan()
    start_color_sensor(brick, port, color_readings)
    while True:
        value = color_readings.recv()
        message_type = 'color_' + value[0]
        message_data = {'data': value[1]}
        socketio.emit(message_type, message_data)
        print('emitted', message_type, message_data)
        socketio.sleep(0.2)


def read_infrared_sensor(port):
    infrared_readings = goless.chan()
    start_infrared_sensor(brick, port, infrared_readings)
    while True:
        value = infrared_readings.recv()
        message_type = 'infrared_' + value[0]
        message_data = {'data': value[1]}
        socketio.emit(message_type, message_data)
        print('emitted', message_type, message_data)
        socketio.sleep(0.2)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('connect')
def robot_connect():
    print('client connected')


@socketio.on('disconnect')
def robot_disconnect():
    print('client disconnected')
    brick.reset_all()


@socketio.on('ping')
def ping_pong():
    emit('pong')


@socketio.on('start_touch_sensor')
def start_touch_sensor_thread(message):
    port = ports[message['port']]
    if port not in sensor_ports:
        emit('error', {'data': 'invalid port for touch sensor: ' + message['port']})
    else:
        global touch_sensor_thread
        with thread_lock:
            if touch_sensor_thread is None:
                touch_sensor_thread = socketio.start_background_task(target=read_touch_sensor, port=port)
        emit('touch_sensor_started', {'data': True})


@socketio.on('start_color_sensor')
def start_color_sensor_thread(message):
    port = ports[message['port']]
    if port not in sensor_ports:
        emit('error', {'data': 'invalid port for color sensor: ' + message['port']})
    else:
        global color_sensor_thread
        with thread_lock:
            if color_sensor_thread is None:
                color_sensor_thread = socketio.start_background_task(target=read_color_sensor, port=port)
        emit('color_sensor_started', {'data': True})


@socketio.on('start_infrared_sensor')
def start_infrared_sensor_thread(message):
    port = ports[message['port']]
    if port not in sensor_ports:
        emit('error', {'data': 'invalid port for infrared sensor: ' + message['port']})
    else:
        global infrared_sensor_thread
        with thread_lock:
            if infrared_sensor_thread is None:
                infrared_sensor_thread = socketio.start_background_task(target=read_infrared_sensor, port=port)
        emit('infrared_sensor_started', {'data': True})

@socketio.on('set_motor_speed')
def set_motor_power(message):
    port = ports[message['port']]
    speed = message['speed']
    if port not in motor_ports:
        emit('error', {'data': 'invalid port for motor: ' + message['port']})
    elif speed > 100 or speed < -100:
        emit('error', {'data': 'invalid motor power: ' + message['power']})
    else:
        brick.set_motor_power(port, speed)
        motor_encoder = brick.get_motor_encoder(port)
        emit('motor_speed_set', {'data': motor_encoder})

if __name__ == '__main__':
    print('starting socket-io server')
    socketio.run(app, host='0.0.0.0', debug=True)
