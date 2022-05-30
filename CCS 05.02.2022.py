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
    # Starting FEL
    future_event_list = list()
    future_event_list.append({'Event Type': 'Arrival', 'Event Time': 0, 'Customer': 'C1'})
    # fel_maker(future_event_list, 'Arrival', 0)

    return state, future_event_list, data


def exponential(lambd):
    r = random.random()
    return -(1 / lambd) * math.log(r)

def uniform(a, b):
    r = random.random()
    return a + (b - a) * r

def arrival(future_event_list, state, clock, data, customer):
    data['Customers'][customer] = dict()
    data['Customers'][customer]['Arrival Time'] = clock  # track every move of this customer
    if 

    if state['Server Status'] < 3:  # if server is free...
        state['Server Status'] += 1
        fel_maker(future_event_list, 'End of Service', clock, customer)
        data['Customers'][customer]['Time Service Begins'] = clock  # track "every move" of this customer
        data['Cumulative Stats']['Service Starters'] += 1

    else:  # if server is busy -> wait in queue
        data['Cumulative Stats']['Area Under Queue Length Curve'] +=\
            state['Queue Length'] * (clock - data['Last Time Queue Length Changed'])
        state['Queue Length'] += 1
        data['Queue Customers'][customer] = clock  # add this customer to the queue
        data['Last Time Queue Length Changed'] = clock

def end_of_service(future_event_list, state, clock, data, customer):


def simulation(simulation_time):

    while clock < simulation_time:



simulation(1000)