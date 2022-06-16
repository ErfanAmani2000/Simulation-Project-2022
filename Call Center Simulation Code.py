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

    #=================== Data: will save every essential data
    data = dict()
    data['Users'] = dict()
    """ 
    To track each customer's entrance time, service start time, and service end time, 
    service technical start time, and service technical end time, for instance:{1:[22,25,29, null, null]}
    """
    data['Last Time Queue Length Changed'] = dict()  # Needed to calculate area under queue length curve
    data['Last Time Queue Length Changed']['Normal Queue'] = 0
    data['Last Time Queue Length Changed']['Special Queue'] = 0
    data['Last Time Queue Length Changed']['Normal CallBack Queue'] = 0
    data['Last Time Queue Length Changed']['Special CallBack Queue'] = 0
    data['Last Time Queue Length Changed']['Normal Technical Queue'] = 0
    data['Last Time Queue Length Changed']['Special Technical Queue'] = 0
    #
    data['Last Time Server Status Changed'] = dict()  # Needed to calculate area under queue length curve
    data['Last Time Server Status Changed']['Expert'] = 0
    data['Last Time Server Status Changed']['Amateur'] = 0
    data['Last Time Server Status Changed']['Technical'] = 0
    #
    data['Last Time Disruption start'] = -1440
    #
    data['Number Of No Waiting Special User'] = 0
    #
    data['Users To waiting In Tecnical Queue'] = []
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
    data['Cumulative Stats']['Area Under Server Busy time']['Amateur'] = 0
    data['Cumulative Stats']['Area Under Server Busy time']['Expert'] = 0
    data['Cumulative Stats']['Area Under Server Busy time']['Technical'] = 0

    # Starting FEL
    future_event_list = list()
    future_event_list.append({'Event Type': 'Shift Start/End', 'Event Time': 0})
    future_event_list.append({'Event Type': 'Disruption Start', 'Event Time': 0})
    future_event_list.append({'Event Type': 'Month Change', 'Event Time': 0})
    return state, future_event_list, data

def fel_maker(future_event_list, event_type, clock, state, user=None, disruption='No'):
    event_time = 0
    inter_arrival_param = {1:3, 2:1, 3:2}
    service_time_param = {"Amateur":7, "Expert":3}
    disruption_inter_arrival_param = {1:2, 2:0.5, 3:1}

    if event_type == 'Call Start':
        if disruption == 'No':
            event_time = clock + exponential(inter_arrival_param[state['Shift Status']])
        else:
            event_time = clock + exponential(disruption_inter_arrival_param[state['Shift Status']])

    elif event_type == 'Call End':
        
        event_time = clock + exponential(service_time_param[user[2]])

    elif event_type == 'Technical Call End':
        event_time = clock + exponential(10)

    elif event_type == 'Disruption Start':
        event_time = clock + 1440*random.randint(1, 30) # this needs to be checked
        

    elif event_type == 'Month Change':
        event_time = clock + 30*1440

    elif event_type == 'Shift Start/End':
        event_time = clock + 480

    new_event = {'Event Type': event_type, 'Event Time': event_time, 'User': user}
    future_event_list.append(new_event)

def exponential(lambda_param):
    r = random.random()
    return -(1 / lambda_param) * math.log(r)

def uniform(a, b):
    r = random.random()
    return a + (b - a) * r

def data_server_calculater(data, state, clock, name):
    data['Cumulative Stats']['Area Under Server Busy time'][name] += (state['{} Server Status'.format(name)] - 1) \
                                                                * (clock - data['Last Time Server Status Changed'][name])
    data['Last Time Server Status Changed'][name] = clock

def data_queue_calculater(data, state, clock, name):
    data['Cumulative Stats']['Area Under Queue Length Curve']['{} Queue'.format(name)] += (state['{} Queue'.format(name)] - 1) \
                                                                * (clock - data['Last Time Queue Length Changed']['{} Queue'.format(name)])
    data['Last Time Queue Length Changed']['{} Queue'.format(name)] = clock
    data['Maximum Queue Length']['{} Queue'.format(name)] = max(data['Maximum Queue Length']['{} Queue'.format(name)],state['{} Queue'.format(name)])

def call_start(future_event_list, state, clock, data, user):
    data['Users'][user[0]] = [clock, 0, 0, None, None]#########

    if user[1] == 'Normal':
        if state['Amateur Server Status'] == 3:
            if state['Expert Server Status'] < 2:
                state['Expert Server Status'] += 1
                user[2] = 'Expert'
                fel_maker(future_event_list, 'Call End', clock, state, user)
                data_server_calculater(data, state, clock, 'Expert')
                data['Users'][user[0]][1] = clock

                
            else:
                state['Normal Queue'] += 1
                if state['Normal Queue'] >= 4:
                    if random.random() <= 0.5:
                        state['Normal Queue'] -= 1
                        state['Normal CallBack Queue'] += 1
                        data_queue_calculater(data, state, clock, 'Normal CallBack')
                        data['Users'][user[0]][1] = clock
                    else:
                        data_queue_calculater(data, state, clock, 'Normal')
        else:
            state['Amateur Server Status'] += 1
            user[2] = 'Amateur'
            fel_maker(future_event_list, 'Call End', clock, state, user)
            data_server_calculater(data, state, clock, 'Amateur')
            data['Users'][user[0]][1] = clock

            
    else:
        if state['Expert Server Status'] < 2:
            state['Expert Server Status'] += 1
            user[2] = 'Expert'
            fel_maker(future_event_list, 'Call End', clock, state, user)
            data_server_calculater(data, state, clock, 'Expert')
            data['Users'][user[0]][1] = clock

            data['Number Of No Waiting Special User'] += 1
        else:
            state['Special Queue'] += 1
            if state['Special Queue'] >= 4:
                if random.random() <= 0.5:
                    state['Special Queue'] -= 1
                    state['Special CallBack Queue'] += 1
                    data_queue_calculater(data, state, clock, 'Special CallBack')
                else:
                    if random.random() <= 0.15:
                        fel_maker(future_event_list, 'Queue Quit', clock, state, user)
                data_queue_calculater(data, state, clock, 'Special')
    new_user = [user[0] + 1, '', '', 0]
    if random.random() <= 0.3:
        new_user[1] = 'Special'
        new_user[2] = 'Expert'
    else:
        new_user[1] = 'Normal'
    if clock >= data['Last Time Disruption start'] + 1440 :
        fel_maker(future_event_list, 'Call Start', clock, state, new_user, disruption='No')
    else:
        fel_maker(future_event_list, 'Call Start', clock, state, new_user, disruption='Yes')

def call_end(future_event_list, state, clock, data, user):
    data['Users'][user[0]][2] = clock
    if user[3] ==1:
        for indx in future_event_list:
            if indx["User"][0] == user[0]:
                break
        future_event_list.remove(indx)
    if random.random() < 0.15:
        if  state['Technical Server Status'] ==2:
            if user[1] == 'Normal':
                state['Normal Technical Queue'] += 1

                data_queue_calculater(data, state, clock, 'Normal Technical')
                data['Users To waiting In Tecnical Queue'].append(user[0])

            elif user[1] == 'Special':
                state['Special Technical Queue'] += 1

                data_queue_calculater(data, state, clock, 'Special Technical')
                data['Users To waiting In Tecnical Queue'].append(user[0])
        elif state['Technical Server Status'] < 2 :
            state['Technical Server Status'] += 1
            fel_maker(future_event_list, 'Technical Call End', clock, state, user[0])
            data_server_calculater(data, state, clock, 'Technical Server')
            data['Users'][user[0]][3] = clock
    if user[2] == 'Expert':
        if state['Special Queue'] >0:
            state['Special Queue'] -=1
            user[2] = 'Expert'#######################
            fel_maker(future_event_list, 'Call End', clock, state, user)
            data_queue_calculater(data, state, clock, 'Special')
            data['Users'][user[0]][1] = clock
        else:
            if state['Normal Queue'] == 0:
                if (state['Shift Status'] ==2) or (state['Shift Status'] ==3):
                    if state['Special CallBack Queue'] > 0:
                        state['Special CallBack Queue'] -=1
                        fel_maker(future_event_list, 'Call End', clock, state, user)
                        data_queue_calculater(data, state, clock, 'Special CallBack')
                        data['Users'][user[0]][1] = clock
                    else:
                        if state['Normal CallBack Queue'] > 0:
                            state['Normal CallBack Queue'] -=1
                            fel_maker(future_event_list, 'Call End', clock, state, user)
                            data_queue_calculater(data, state, clock, 'normal CallBack')
                            data['Users'][user[0]][1] = clock
                        else:
                            state['Expert Server Status'] -=1
                            data_server_calculater(data, state, clock, 'Expert')
                else:
                    state['Expert Server Status'] -=1
                    data_server_calculater(data, state, clock, 'Expert')
            else:
                state['Normal Queue'] -=1
                fel_maker(future_event_list, 'Call End', clock, state, user)
                data_queue_calculater(data, state, clock, 'normal')
                data['Users'][user[0]][1] = clock
                
    elif user[2] == 'Amateur':
        if state['Normal Queue'] > 0:
            state['Normal Queue'] -= 1
            fel_maker(future_event_list, 'Call End', clock, state, user)
            data_queue_calculater(data, state, clock, 'normal')
            data['Users'][user[0]][1] = clock
        else:
            if state['Shift Status'] ==2 or state['Shift Status'] ==3:
                if state['Normal CallBack Queue'] > 0:
                    state['Normal CallBack Queue'] -=1
                    fel_maker(future_event_list, 'Call End', clock, state, user)
                    data_queue_calculater(data, state, clock, 'normal CallBack')
                    data['Users'][user[0]][1] = clock
                else:
                    state['Amateur Server Status'] -=1
                    data_server_calculater(data, state, clock, 'Amateur')
            else:
                state['Amateur Server Status'] -=1
                data_server_calculater(data, state, clock, 'Amateur')

def technical_call_end(future_event_list, state, clock, data, user):
    data['Users'][user][4] = clock
    if state['Special Technical Queue'] == 0:
        if state['Normal Technical Queue'] == 0:
            state['Technical Server Status'] += 1
            
        else:
            state['Normal Technical Queue'] -= 1
            
            temp = data['Users To waiting In Tecnical Queue'].pop(0)
            data['Users'][temp][3] = clock
            fel_maker(future_event_list, 'Technical Call End', clock, state, temp)
    else:
        state['Special Technical Queue'] -= 1
        
        temp = data['Users To waiting In Tecnical Queue'].pop(0)
        data['Users'][temp][3] = clock
        fel_maker(future_event_list, 'Technical Call End', clock, state, temp)

def disruption_start(clock, data):
    data['Last Time Disruption start'] = clock

def month_change(future_event_list, state, clock, user):
    fel_maker(future_event_list, 'Disruption Start', clock, state, user, disruption='Yes')
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

    while clock < simulation_time

simulation(1000)

#====================================Calculate of the KPI






