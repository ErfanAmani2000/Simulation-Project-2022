import random
import math
import pandas as pd

def starting_state():

    state = dict()
    state['Normal Queue'] = 0
    state['Special Queue'] = 0
    state['Normal CallBack Queue'] = 0
    state['Special CallBack Queue'] = 0
    state['Expert Server Status'] = 0
    state['Amateur Server Status'] = 0
    state['Technical Server Status'] = 0
    state['Special Technical Queue'] = 0
    state['Normal Technical Queue'] = 0
    state['Shift Status'] = 0

    data = dict()

    return state, future_event_list, data


def exponential(lambd):
    r = random.random()
    return -(1 / lambd) * math.log(r)

def uniform(a, b):
    r = random.random()
    return a + (b - a) * r

def arrival(future_event_list, state, clock, data, customer):


def end_of_service(future_event_list, state, clock, data, customer):


def simulation(simulation_time):

    while clock < simulation_time:



simulation(1000)