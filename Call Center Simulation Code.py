import random
import math

def starting_state():

    # State variables
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

    # Data: will save every essential data
    data = dict()
    data['Customers'] = dict()

    # Cumulative Stats
    data['Cumulative Stats'] = dict()
    data['Cumulative Stats'][] = 0 # this needs to be completed

    # Starting FEL
    future_event_list = list()
    future_event_list.append({'Event Type': 'Shift Start/End', 'Event Time': 0})
    future_event_list.append({'Event Type': 'Disruption Start', 'Event Time': 0})
    future_event_list.append({'Event Type': 'Month Change', 'Event Time': 0})
    return state, future_event_list, data

def fel_maker(future_event_list, event_type, clock, customer=None):
    event_time = 0
    inter_arrival_param = {1:3, 2:1, 3:2}
    service_time_param = {"Amateur":3, "Expert":7, "Technical":10}

    if event_type == 'Call Start':
        event_time = clock + exponential(inter_arrival_param[state['Shift Status']])

    elif event_type == 'Call End':
        event_time = clock + exponential(service_time_param[])

    elif event_type == 'Technical Call End':
        event_time = clock + exponential(10)

    elif event_type == 'Disruption End':
        event_time = clock + 1440

    elif event_type == 'Disruption Start':
        event_time = clock + random.randint(1, 30) # this should be double checked

    elif event_type == 'Month Change':
        event_time = clock + 30*1440

    elif event_type == 'Shift Start/End':
        event_time = clock + 480

    new_event = {'Event Type': event_type, 'Event Time': event_time, 'Customer': customer}
    future_event_list.append(new_event)

def exponential(lambd):
    r = random.random()
    return -(1 / lambd) * math.log(r)

def uniform(a, b):
    r = random.random()
    return a + (b - a) * r

def call_start(future_event_list, state, clock, data, customer):
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

def call_end(future_event_list, state, clock, data, customer):



def technical_call_end(future_event_list, state, clock, data, customer):



def disruption_start(future_event_list, state, clock, data, customer):



def disruption_end(future_event_list, state, clock, data, customer):



def month_change(future_event_list, state, clock, data, customer):



def queue_quit(future_event_list, state, clock, data, customer):



def shift_start_end(future_event_list, state, clock, data, customer):



def simulation(simulation_time):

    while clock < simulation_time:



simulation(1000)