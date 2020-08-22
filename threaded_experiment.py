"""Example of multithreaded code to read sensors at a specified time interval.

TheBobPlus, August 2020.
"""

import threading
from threading import Event
from queue import Queue
import time
from random import random

# Parameters -----------------------------------------------------------------

# Dictionary of sensors (and their time to read data in seconds)
sensor_times = {'sensor1': 0.5,
                'sensor2': 1}

dt_check = 0.1  # time delay to periodically probe if events are happening
                # (NOT the data recording rate), in seconds

dt_record = 2  # data recodring rate (in seconds) 


# Basic functions ------------------------------------------------------------


def sensor_read(t):
    """simulates a sensor that takes a time t (in s) to read"""
    time.sleep(t)
    return random()


def save_data(sensor, data):
    """define here how data is saved depending on the sensor."""
    print(f'Data saved for {sensor}: {data}')
    pass


# Functions that will be threaded --------------------------------------------


def clock(dt, events):
    """clock that sets events every dt (in s)."""
    while True:
        for event in events.values():
            event.set()
        time.sleep(dt)


def sensor_reading(sensor, event, queue):
    """Read data from sensor and put it into queue when event is set."""
    while True:
        if event.is_set():
            t = sensor_times[sensor]
            data = sensor_read(t)
            queue.put((sensor, data))
            event.clear()
        time.sleep(dt_check)  # avoids overloading processor 

def data_management(queue):
    """Get data from all sensors and decide what to do with it."""
    while True:
        while queue.qsize() > 0:
            sensor, data = queue.get()
            save_data(sensor, data)
            # Add any other 
        time.sleep(dt_check)


# Main program ---------------------------------------------------------------

def main():

    sensors = sensor_times.keys()
    queue = Queue()  # data sharing queue

    events = {}   # one event per sensor
    threads = []  

    # Sensor reading threads
    for sensor in sensors:
        event = Event()
        events[sensor] = event
        thread = threading.Thread(target=sensor_reading,
                                args=(sensor, event, queue))
        threads.append(thread)

    # Add clock and data management threads
    c_thread = threading.Thread(target=clock, args=(dt_record, events))
    threads.append(c_thread)
    d_thread = threading.Thread(target=data_management, args=(queue,))
    threads.append(d_thread)

    for thread in threads:
        thread.start()

    # Since the program runs forever, no needs to join threads here

if __name__ == '__main__':
    main()
