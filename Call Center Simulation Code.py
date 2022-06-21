import random
import math


def starting_state():
    # State variables declaration
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
    data['Users'] = dict()
    """ 
    Users dictionary is implemented to track each customer's entrance time, service start time, and service end time, 
    service technical start time, and service technical end time, for instance:{1:[22, 25, 29, null, null]}. It is
    noteworthy to mention that not all the users use technical service so the 4th and 5th elements of each list is set
    to null for initialization.
    """
    # The dictionary below is needed to store the last time for which each queue has changed in length.
    data['Last Time Queue Length Changed'] = dict()
    data['Last Time Queue Length Changed']['Normal Queue'] = 0
    data['Last Time Queue Length Changed']['Special Queue'] = 0
    data['Last Time Queue Length Changed']['Normal CallBack Queue'] = 0
    data['Last Time Queue Length Changed']['Special CallBack Queue'] = 0
    data['Last Time Queue Length Changed']['Normal Technical Queue'] = 0
    data['Last Time Queue Length Changed']['Special Technical Queue'] = 0

    # The dictionary below is needed to store the last length of each queue.
    data['Last Queue Length'] = dict()
    data['Last Queue Length']['Normal Queue'] = 0
    data['Last Queue Length']['Special Queue'] = 0
    data['Last Queue Length']['Normal CallBack Queue'] = 0
    data['Last Queue Length']['Special CallBack Queue'] = 0
    data['Last Queue Length']['Normal Technical Queue'] = 0
    data['Last Queue Length']['Special Technical Queue'] = 0

    # The dictionary below is needed to store the last time for which each server status has been changed.
    data['Last Time Server Status Changed'] = dict()
    data['Last Time Server Status Changed']['Expert'] = 0
    data['Last Time Server Status Changed']['Amateur'] = 0
    data['Last Time Server Status Changed']['Technical'] = 0

    # The dictionary below is needed to store the last server status.
    data['Last Server Status'] = dict()
    data['Last Server Status']['Expert'] = 0
    data['Last Server Status']['Amateur'] = 0
    data['Last Server Status']['Technical'] = 0

    # These crumb data are stored for the purpose that is obviously expressed.
    data['Last Time Disruption start'] = -1440
    data['Number Of No Waiting Special User'] = 0
    data['Users To waiting In Technical Queue'] = []
    data['Number of special users'] = 0

    # The dictionary below is needed to store the maximum length of each queue during the simulation.
    data['Maximum Queue Length'] = dict()
    data['Maximum Queue Length']['Normal Queue'] = 0
    data['Maximum Queue Length']['Special Queue'] = 0
    data['Maximum Queue Length']['Normal CallBack Queue'] = 0
    data['Maximum Queue Length']['Special CallBack Queue'] = 0
    data['Maximum Queue Length']['Normal Technical Queue'] = 0
    data['Maximum Queue Length']['Special Technical Queue'] = 0

    # The dictionary below is needed to store the maximum waiting time of users in each queue during the simulation.
    data['Maximum Waiting time'] = dict()
    data['Maximum Waiting time']['Normal Queue'] = 0
    data['Maximum Waiting time']['Special Queue'] = 0
    data['Maximum Waiting time']['Normal CallBack Queue'] = 0
    data['Maximum Waiting time']['Special CallBack Queue'] = 0
    data['Maximum Waiting time']['Normal Technical Queue'] = 0
    data['Maximum Waiting time']['Special Technical Queue'] = 0

    # Cumulative statistics that are necessary to assess the system performance measures.
    data['Cumulative Stats'] = dict()
    data['Cumulative Stats']['Special Users System Duration time'] = 0
    data['Cumulative Stats']['Number of Special Users with no Delay'] = 0
    data['Cumulative Stats']['Number of Special Users'] = 0

    # This specific dictionary in cumulative stats is assigned to store area under each queue length curve.
    data['Cumulative Stats']['Area Under Queue Length Curve'] = dict()
    data['Cumulative Stats']['Area Under Queue Length Curve']['Normal Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Special Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Normal CallBack Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Special CallBack Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Normal Technical Queue'] = 0
    data['Cumulative Stats']['Area Under Queue Length Curve']['Special Technical Queue'] = 0

    # This specific dictionary in cumulative stats is assigned to store area under waiting time for users in each queue.
    data['Cumulative Stats']['Area Under Waiting time'] = dict()
    data['Cumulative Stats']['Area Under Waiting time']['Normal Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Special Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Normal CallBack Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Special CallBack Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Normal Technical Queue'] = 0
    data['Cumulative Stats']['Area Under Waiting time']['Special Technical Queue'] = 0

    # This specific dictionary in cumulative stats is assigned to store area under each server busy time.
    data['Cumulative Stats']['Area Under Server Busy time'] = dict()
    data['Cumulative Stats']['Area Under Server Busy time']['Amateur'] = 0
    data['Cumulative Stats']['Area Under Server Busy time']['Expert'] = 0
    data['Cumulative Stats']['Area Under Server Busy time']['Technical'] = 0

    # FEL initialization, and Starting events that initialize the simulation
    future_event_list = list()
    future_event_list.append({'Event Type': 'Shift Start/End', 'Event Time': 0, 'User': ''})
    future_event_list.append({'Event Type': 'Disruption Start', 'Event Time': 0, 'User': ''})
    future_event_list.append({'Event Type': 'Month Change', 'Event Time': 0, 'User': ''})
    future_event_list.append({'Event Type': 'Call Start', 'Event Time': 0, 'User': [1, 'Special', 'Expert', 0]})
    return state, future_event_list, data


def fel_maker(future_event_list: list, event_type: str, clock: float, state: dict, user: list = None,
              disruption: str = 'No'):
    """
    This function is supposed to set the next event into future event list

    param future_event_list: list that contains all future events
    param event_type: types of each event that can occur in this simulation
    param clock: simulation clock
    param state: dictionary that contains all state variables
    param user: a list that filled with each user's attributes
    param disruption: whether the next event is set in disruption conditions or not
    """
    event_time = 0
    inter_arrival_param = {1: 1 / 3, 2: 1, 3: 1 / 2}
    disruption_inter_arrival_param = {1: 1 / 2, 2: 2, 3: 1}
    service_time_param = {"Amateur": 1 / 7, "Expert": 1 / 3}

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
        event_time = clock + 1440 * random.randint(1, 30)

    elif event_type == 'Month Change':
        event_time = clock + 30 * 1440

    elif event_type == 'Shift Start/End':
        event_time = clock + 480

    new_event = {'Event Type': event_type, 'Event Time': event_time, 'User': user}
    future_event_list.append(new_event)


def exponential(lambda_param: float) -> float:
    """
    param lambda_param: mean parameter of exponential distribution
    return: random variate that conforms to exponential distribution
    """
    r = random.random()
    return -(1 / lambda_param) * math.log(r)


def uniform(a: float, b: float) -> float:
    """
    param a: lower bound for uniform dist.
    param b: upper bound for uniform dist.
    return: random variate that obey uniform dist.
    """
    r = random.random()
    return a + (b - a) * r


def discrete_uniform(a: int, b: int) -> int:
    """
    param a: lower bound for discrete uniform dist.
    param b: upper bound for discrete uniform dist.
    return: random variate that obey discrete uniform dist.
    """
    r = random.random()
    for inc in range(a, b + 1):
        if (r < (inc + 1) / (b - a + 1)) and (r >= inc / (b - a + 1)):
            print(r)
            return inc


def data_server_calculater(data: dict, state: dict, clock: float, name: str):
    """
    This function is supposed to calculate area under each server busy time.

    param data: the dictionary that store every essential data
    param name: each server name, whether is expert, amateur or technical
    """
    data['Cumulative Stats']['Area Under Server Busy time'][name] += state['{} Server Status'.format(name)] \
                                                            * (clock - data['Last Time Server Status Changed'][name])
    data['Last Time Server Status Changed'][name] = clock


def data_queue_calculater(data: dict, state: dict, clock: float, name: str):
    """
    This function is supposed to calculate area under each queue length curve,
    and also the maximum queue length.
    """
    data['Cumulative Stats']['Area Under Queue Length Curve']['{} Queue'.format(name)] += state['{} Queue'.format(name)]\
                                            * (clock - data['Last Time Queue Length Changed']['{} Queue'.format(name)])
    data['Last Time Queue Length Changed']['{} Queue'.format(name)] = clock
    data['Maximum Queue Length']['{} Queue'.format(name)] = max(data['Maximum Queue Length']['{} Queue'.format(name)],
                                                                state['{} Queue'.format(name)])


def call_start(future_event_list: list, state: dict, clock: float, data: dict, user: list):
    """
    This function is supposed to implement call start event that is fully described in project's report.
    """
    data['Users'][user[0]] = [clock, 0, 0, None, None]

    if user[1] == 'Normal':  # if a normal user call ...
        if state['Amateur Server Status'] == 3:  # if all amateur server are busy ...
            if state['Expert Server Status'] < 2:  # if at least one expert server is free ...
                data['Last Server Status']['Expert'] = state['Expert Server Status']
                state['Expert Server Status'] += 1
                user[2] = 'Expert'
                fel_maker(future_event_list, 'Call End', clock, state, user)
                data_server_calculater(data, state, clock, 'Expert')
                data['Users'][user[0]][1] = clock

            else:  # if all expert servers are also busy at the time ...
                data['Last Queue Length']['Normal Queue'] = state['Normal Queue']
                state['Normal Queue'] += 1

                if state['Normal Queue'] >= 4:  # if normal queue length is more than 4 ...
                    if random.random() <= 0.5:  # in order to make half of users
                        data['Last Queue Length']['Normal Queue'] = state['Normal Queue']
                        state['Normal Queue'] -= 1
                        data['Last Queue Length']['Normal Queue'] = state['Normal CallBack Queue']
                        state['Normal CallBack Queue'] += 1
                        data_queue_calculater(data, state, clock, 'Normal CallBack')
                        data['Users'][user[0]][1] = clock
                    else:
                        data_queue_calculater(data, state, clock, 'Normal')
        else:
            data['Last Server Status']['Amateur'] = state['Amateur Server Status']
            state['Amateur Server Status'] += 1
            user[2] = 'Amateur'
            fel_maker(future_event_list, 'Call End', clock, state, user)
            data_server_calculater(data, state, clock, 'Amateur')
            data['Users'][user[0]][1] = clock

    else:
        data['Number of special users'] += 1
        if state['Expert Server Status'] < 2:
            data['Last Server Status']['Expert'] = state['Expert Server Status']
            state['Expert Server Status'] += 1
            user[2] = 'Expert'
            fel_maker(future_event_list, 'Call End', clock, state, user)
            data_server_calculater(data, state, clock, 'Expert')
            data['Users'][user[0]][1] = clock

            data['Number Of No Waiting Special User'] += 1
        else:
            data['Last Queue Length']['Special Queue'] = state['Special Queue']
            state['Special Queue'] += 1
            if state['Special Queue'] >= 4:
                if random.random() <= 0.5:
                    data['Last Queue Length']['Special Queue'] = state['Special Queue']
                    state['Special Queue'] -= 1
                    data['Last Queue Length']['Special CallBack Queue'] = state['Special CallBack Queue']
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
    if clock >= data['Last Time Disruption start'] + 1440:
        fel_maker(future_event_list, 'Call Start', clock, state, new_user, disruption='No')
    else:
        fel_maker(future_event_list, 'Call Start', clock, state, new_user, disruption='Yes')


def call_end(future_event_list, state, clock, data, user):
    data['Users'][user[0]][2] = clock
    if user[3] == 1:
        for index in future_event_list:
            if index["User"][0] == user[0]:
                break
            future_event_list.remove(index)
    if random.random() < 0.15:
        if state['Technical Server Status'] == 2:
            if user[1] == 'Normal':
                data['Last Queue Length']['Normal Technical Queue'] = state['Normal Technical Queue']
                state['Normal Technical Queue'] += 1

                data_queue_calculater(data, state, clock, 'Normal Technical')
                data['Users To waiting In Technical Queue'].append(user[0])

            elif user[1] == 'Special':
                data['Last Queue Length']['Special Technical Queue'] = state['Special Technical Queue']
                state['Special Technical Queue'] += 1

                data_queue_calculater(data, state, clock, 'Special Technical')
                data['Users To waiting In Technical Queue'].append(user[0])
        elif state['Technical Server Status'] < 2:
            data['Last Server Status']['Technical'] = state['Technical Server Status']
            state['Technical Server Status'] += 1
            fel_maker(future_event_list, 'Technical Call End', clock, state, user[0])
            data_server_calculater(data, state, clock, 'Technical')
            data['Users'][user[0]][3] = clock
    if user[2] == 'Expert':
        if state['Special Queue'] > 0:
            data['Last Queue Length']['Special Queue'] = state['Special Queue']
            state['Special Queue'] -= 1
            user[2] = 'Expert'
            fel_maker(future_event_list, 'Call End', clock, state, user)
            data_queue_calculater(data, state, clock, 'Special')
            data['Users'][user[0]][1] = clock
        else:
            if state['Normal Queue'] == 0:
                if (state['Shift Status'] == 2) or (state['Shift Status'] == 3):
                    if state['Special CallBack Queue'] > 0:
                        data['Last Queue Length']['Special CallBack Queue'] = state['Special CallBack Queue']
                        state['Special CallBack Queue'] -= 1
                        fel_maker(future_event_list, 'Call End', clock, state, user)
                        data_queue_calculater(data, state, clock, 'Special CallBack')
                        data['Users'][user[0]][1] = clock
                    else:
                        if state['Normal CallBack Queue'] > 0:
                            data['Last Queue Length']['Normal CallBack Queue'] = state['Normal CallBack Queue']
                            state['Normal CallBack Queue'] -= 1
                            fel_maker(future_event_list, 'Call End', clock, state, user)
                            data_queue_calculater(data, state, clock, 'Normal CallBack')
                            data['Users'][user[0]][1] = clock
                        else:
                            data['Last Server Status']['Expert'] = state['Expert Server Status']
                            state['Expert Server Status'] -= 1
                            data_server_calculater(data, state, clock, 'Expert')
                else:
                    data['Last Server Status']['Expert'] = state['Expert Server Status']
                    state['Expert Server Status'] -= 1
                    data_server_calculater(data, state, clock, 'Expert')
            else:
                data['Last Queue Length']['Normal Queue'] = state['Normal Queue']
                state['Normal Queue'] -= 1
                fel_maker(future_event_list, 'Call End', clock, state, user)
                data_queue_calculater(data, state, clock, 'Normal')
                data['Users'][user[0]][1] = clock

    elif user[2] == 'Amateur':
        if state['Normal Queue'] > 0:
            data['Last Queue Length']['Normal Queue'] = state['Normal Queue']
            state['Normal Queue'] -= 1
            fel_maker(future_event_list, 'Call End', clock, state, user)
            data_queue_calculater(data, state, clock, 'Normal')
            data['Users'][user[0]][1] = clock
        else:
            if state['Shift Status'] == 2 or state['Shift Status'] == 3:
                if state['Normal CallBack Queue'] > 0:
                    state['Normal CallBack Queue'] -= 1
                    fel_maker(future_event_list, 'Call End', clock, state, user)
                    data_queue_calculater(data, state, clock, 'Normal CallBack')
                    data['Users'][user[0]][1] = clock
                else:
                    data['Last Server Status']['Amateur'] = state['Amateur Server Status']
                    state['Amateur Server Status'] -= 1
                    data_server_calculater(data, state, clock, 'Amateur')
            else:
                data['Last Server Status']['Amateur'] = state['Amateur Server Status']
                state['Amateur Server Status'] -= 1
                data_server_calculater(data, state, clock, 'Amateur')


def technical_call_end(future_event_list, state, clock, data, user):
    data['Users'][user][4] = clock
    if state['Special Technical Queue'] == 0:
        if state['Normal Technical Queue'] == 0:
            data['Last Server Status']['Technical'] = state['Technical Server Status']
            state['Technical Server Status'] -= 1

        else:
            data['Last Queue Length']['Normal Technical Queue'] = state['Normal Technical Queue']
            state['Normal Technical Queue'] -= 1

            temp = data['Users To waiting In Technical Queue'].pop(0)
            data['Users'][temp][3] = clock
            fel_maker(future_event_list, 'Technical Call End', clock, state, temp)
    else:
        data['Last Queue Length']['Special Technical Queue'] = state['Special Technical Queue']
        state['Special Technical Queue'] -= 1

        temp = data['Users To waiting In Technical Queue'].pop(0)
        data['Users'][temp][3] = clock
        fel_maker(future_event_list, 'Technical Call End', clock, state, temp)


def disruption_start(clock, data):
    data['Last Time Disruption start'] = clock


def month_change(future_event_list, state, clock):
    fel_maker(future_event_list, 'Disruption Start', clock, state, disruption='Yes')
    fel_maker(future_event_list, 'Month Change', clock, state)


def queue_quit(state, user, data):
    if user[1] == 'Normal':
        data['Last Queue Length']['Normal Queue'] = state['Normal Queue']
        state['Normal Queue'] -= 1
    else:
        data['Last Queue Length']['Special Queue'] = state['Special Queue']
        state['Special Queue'] -= 1


def shift_start_end(future_event_list, state, clock):
    if clock % 1440 < 480:
        state['Shift Status'] = 1
    elif (clock % 1440 >= 480) and (clock % 1440 < 960):
        state['Shift Status'] = 2
    else:
        state['Shift Status'] = 3
    fel_maker(future_event_list, 'Shift Start/End', clock, state)


def simulation(simulation_time):
    state, future_event_list, data = starting_state()
    clock = 0
    future_event_list.append({'Event Type': 'Shift Start/End', 'Event Time': simulation_time, 'User': ''})
    while clock < simulation_time:
        sorted_fel = sorted(future_event_list, key=lambda x: x['Event Time'])
        current_event = sorted_fel[0]  # find imminent event
        clock = current_event['Event Time']  # advance time
        user = current_event['User']  # find the customer of that event

        if clock < simulation_time:
            if current_event['Event Type'] == 'Call Start':
                call_start(future_event_list, state, clock, data, user)
            elif current_event['Event Type'] == 'Call End':
                call_end(future_event_list, state, clock, data, user)
            elif current_event['Event Type'] == 'Technical Call End':
                technical_call_end(future_event_list, state, clock, data, user)
            elif current_event['Event Type'] == 'Disruption Start':
                disruption_start(clock, data)
            elif current_event['Event Type'] == 'Month Change':
                month_change(future_event_list, state, clock)
            elif current_event['Event Type'] == 'Queue Quit':
                queue_quit(state, user, data)
            elif current_event['Event Type'] == 'Shift Start/End':
                shift_start_end(future_event_list, state, clock)

            future_event_list.remove(current_event)
        else:
            future_event_list.clear()
    return data, state


data, state = simulation(43200)


def calculate_kpi(data, simulation_time):
    server_number = {"Amateur": 3, "Expert": 2, "Technical": 2}
    kpi_results = dict()

    kpi_results['Special Users in system duration'] = 0
    for i in data['Users'].keys():
        if data['Users'][i][3] is None:
            kpi_results['Special Users in system duration'] += data['Users'][i][2] - data['Users'][i][0]
        else:
            kpi_results['Special Users in system duration'] += data['Users'][i][4] - data['Users'][i][0]
    kpi_results['Special Users in system duration'] = kpi_results['Special Users in system duration'] /\
                                                     data['Number of special users']

    kpi_results['Average Queue Length'] = {}
    for i in data['Cumulative Stats']['Area Under Queue Length Curve'].keys():
        kpi_results['Average Queue Length'][i] = data['Cumulative Stats']['Area Under Queue Length Curve'][i] / simulation_time

    kpi_results['Max Queue Length'] = {}
    for i in data['Maximum Queue Length'].keys():
        kpi_results['Max Queue Length'][i] = data['Maximum Queue Length'][i]

    kpi_results['Average Queue Time'] = {}
    for i in data['Cumulative Stats']['Area Under Waiting time'].keys():
        kpi_results['Average Queue Time'][i] = data['Cumulative Stats']['Area Under Waiting time'][i] / simulation_time

    kpi_results['Max Queue Time'] = {}
    for i in data['Maximum Waiting time'].keys():
        kpi_results['Max Queue Time'][i] = data['Maximum Waiting time'][i]

    kpi_results['Server Utilization'] = {}
    for i in data['Cumulative Stats']['Area Under Server Busy time'].keys():
        kpi_results['Server Utilization'][i] = data['Cumulative Stats']['Area Under Server Busy time'][i] /\
                                               (simulation_time*server_number[i])

    return kpi_results


kpi_result = calculate_kpi(data, 43200)

print(kpi_result)
a = data['Users'][25000][0]
b = data['Users'][25000][2]
print(b - a)
print(data["Users"])
