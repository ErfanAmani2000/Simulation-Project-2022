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
    data['Users'] = dict()  # To track each customer, saving their arrival time, time service begins, etc.
    #
    data['Last Time Queue Length Changed'] = dict()  # Needed to calculate area under queue length curve
    data['Last Time Queue Length Changed']['Normal Queue'] = 0
    data['Last Time Queue Length Changed']['Special Queue'] = 0
    data['Last Time Queue Length Changed']['Normal CallBack Queue'] = 0
    data['Last Time Queue Length Changed']['Special CallBack Queue'] = 0
    data['Last Time Queue Length Changed']['Normal Technical Queue'] = 0
    data['Last Time Queue Length Changed']['Special Technical Queue'] = 0
    #
    data['Maximum Queue Length'] = dict()
    data['Maximum Queue Length']['Normal Queue'] = 0
    data['Maximum Queue Length']['Special Queue'] = 0
    data['Maximum Queue Length']['Normal CallBack Queue'] = 0
    data['Maximum Queue Length']['Special CallBack Queue'] = 0
    data['Maximum Queue Length']['Normal Technical Queue'] = 0
    data['Maximum Queue Length']['Special Technical Queue'] = 0
    #
    data['Maximum Waiting time'] = dict()
    data['Maximum Waiting time']['Normal Queue'] = 0
    data['Maximum Waiting time']['Special Queue'] = 0
    data['Maximum Waiting time']['Normal CallBack Queue'] = 0
    data['Maximum Waiting time']['Special CallBack Queue'] = 0
    data['Maximum Waiting time']['Normal Technical Queue'] = 0
    data['Maximum Waiting time']['Special Technical Queue'] = 0

    # Cumulative Stats
    data['Cumulative Stats'] = dict()
    data['Cumulative Stats']['Special Users System Duration time'] = 0
    data['Cumulative Stats']['Number of Special Users with no Delay'] = 0
    data['Cumulative Stats']['Number of Special Users'] = 0
    #
    data['Cumulative Stats']['Area Under Queue Length Curve'] = dict()
    data['Cumulative Stats']['Area Under Queue Length Curve']['Normal Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Special Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Normal CallBack Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Special CallBack Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Normal Technical Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Special Technical Queue'] = 0
    #
    data['Cumulative Stats']['Area Under Waiting time'] = dict()
    data['Cumulative Stats']['Area Under Waiting time']['Normal Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Special Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Normal CallBack Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Special CallBack Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Normal Technical Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Special Technical Queue'] = 0
    #
    data['Cumulative Stats']['Area Under Server Busy time'] = dict()
    data['Cumulative Stats']['Area Under Server Busy time']['Amateur Servers'] = 0
    data['Cumulative Stats']['Area Under Server Busy time']['Expert Servers'] = 0
    data['Cumulative Stats']['Area Under Server Busy time']['Technical Servers'] = 0

    # Starting FEL
    future_event_list = list()
    future_event_list.append({'Event Type': 'Shift Start/End', 'Event Time': 0})
    future_event_list.append({'Event Type': 'Disruption Start', 'Event Time': 0})
    future_event_list.append({'Event Type': 'Month Change', 'Event Time': 0})
    return state, future_event_list, data

def fel_maker(future_event_list, event_type, clock, state, user=None):
    event_time = 0
    inter_arrival_param = {1:3, 2:1, 3:2}
    service_time_param = {"Amateur":7, "Expert":3, "Technical":10}

    if event_type == 'Call Start':
        event_time = clock + exponential(inter_arrival_param[state['Shift Status']])

    elif event_type == 'Call End':
        event_time = clock + exponential(service_time_param[])

    elif event_type == 'Technical Call End':
        event_time = clock + exponential(10)

    elif event_type == 'Disruption End':
        event_time = clock + 1440

    elif event_type == 'Disruption Start':
        event_time = clock + 1440*random.randint(1, 30) # this needs to be checked

    elif event_type == 'Month Change':
        event_time = clock + 30*1440

    elif event_type == 'Shift Start/End':
        event_time = clock + 480

    new_event = {'Event Type': event_type, 'Event Time': event_time, 'User': user}
    future_event_list.append(new_event)

def exponential(lambd):
    r = random.random()
    return -(1 / lambd) * math.log(r)

def uniform(a, b):
    r = random.random()
    return a + (b - a) * r

def call_start(future_event_list, state, clock, data, user):

    if user[1] == 'Normal':
        if state['Amateur Server Status'] == 3:
            if state['Expert Server Status'] < 2:
                state['Expert Server Status'] += 1
                fel_maker(future_event_list, 'Call End', clock, state, user)
                data['Cumulative Stats']['Area Under Server Busy time']['Expert Servers'] = state['Expert Server Status'] * ( - clock) # this needs to be completed
                fel_maker(future_event_list, 'Call Start', clock, state, user)
            else:
                state['Normal Queue'] += 1
                if state['Normal Queue'] >= 4:
                    if random.random() <= 0.5:
                        state['Normal Queue'] -= 1
                        state['Normal CallBack Queue'] += 1
                        fel_maker(future_event_list, 'Call Start', clock, state, user)
                    else:

                else:
                    fel_maker(future_event_list, 'Call Start', clock, state, user) # this needs to be checked
        else:
            state['Amateur Server Status'] += 1
            fel_maker(future_event_list, 'Call End', clock, state, user)
            fel_maker(future_event_list, 'Call Start', clock, state, user)
    else:
        if state['Expert Server Status'] < 2:
            state['Expert Server Status'] += 1
            fel_maker(future_event_list, 'Call End', clock, state, user)
            fel_maker(future_event_list, 'Call Start', clock, state, user)
        else:
            state['Special Queue'] += 1
            if state['Special Queue'] >= 4:
                if random.random() <= 0.5:
                    state['Special Queue'] -= 1
                    state['Special CallBack Queue'] += 1
                    fel_maker(future_event_list, 'Call Start', clock, state, user)
                else:

            else:
                fel_maker(future_event_list, 'Call Start', clock, state, user)

def call_end(future_event_list, state, clock, data, user):
        if user[3] == 0:

        else:
            future_event_list


def technical_call_end(future_event_list, state, clock, data, user):
    if state['Special Technical Queue'] == 0:
        if state['Normal Technical Queue'] == 0:
            state['Technical Server Status'] += 1
        else:
            state['Normal Technical Queue'] -= 1
            fel_maker(future_event_list, 'Technical Call End', clock, state, user)
    else:
        state['Special Technical Queue'] -= 1
        fel_maker(future_event_list, 'Technical Call End', clock, state, user)


def disruption_start(future_event_list, state, clock, data, user):



def disruption_end(future_event_list, state, clock, data, user):



def month_change(future_event_list, state, clock, data, user):
    fel_maker(future_event_list, 'Disruption Start', clock, state, user)
    fel_maker(future_event_list, 'Month Change', clock, state, user)


def queue_quit(future_event_list, state, clock, data, user):
    if user[1] == 'Normal':
        state['Normal Queue'] -= 1
    else:
        state['Special Queue'] -= 1


def shift_start_end(future_event_list, state, clock, data, user):
    if clock % 1440 < 480:
        state['Shift Status'] = 1
    elif (clock % 1440 >= 480) and (clock % 1440 < 960):
        state['Shift Status'] = 2
    else:
        state['Shift Status'] = 3

    fel_maker(future_event_list, 'Shift Start/End', clock, state, user)


def simulation(simulation_time):

    while clock < simulation_time:

simulation(1000)