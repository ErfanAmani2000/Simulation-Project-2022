from scipy import stats
import random
import math
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

start_time = time.time()


class CallCenterSimulation:
    
    def __init__(self, param_numbeer_of_amateur_server, param_callback_ratio, param_special_porportion, inter_arrival_param, disruption_inter_arrival_param, service_time_param,
                 technical_service_time_param,percent_needtechnical, simulation_time):
        self.inter_arrival_param = inter_arrival_param
        self.disruption_inter_arrival_param = disruption_inter_arrival_param
        self.service_time_param = service_time_param
        self.technical_service_time_param = technical_service_time_param
        self.percent_needtechnical = percent_needtechnical
        self.simulation_time = simulation_time
        self.param_special_porportion = param_special_porportion
        self.param_callback_ratio = param_callback_ratio
        self.param_numbeer_of_amateur_server = param_numbeer_of_amateur_server

        self.clock = 0
        self.trace_list = []


    def setter(self, param_numbeer_of_amateur_server=3, param_callback_ratio=0.5, param_special_porportion=0.3, 
               inter_arrival_param={1: 3, 2: 1, 3: 2}, disruption_inter_arrival_param={1: 2, 2: 1 / 2, 3: 1},
               service_time_param={"Amateur": 7, "Expert": 3}, technical_service_time_param=10, percent_needtechnical=0.15,
               simulation_time=30*24*60):
        self.inter_arrival_param = inter_arrival_param
        self.disruption_inter_arrival_param = disruption_inter_arrival_param
        self.service_time_param = service_time_param
        self.technical_service_time_param = technical_service_time_param
        self.percent_needtechnical = percent_needtechnical
        self.simulation_time = simulation_time
        self.param_special_porportion = param_special_porportion
        self.param_callback_ratio = param_callback_ratio
        self.param_numbeer_of_amateur_server = param_numbeer_of_amateur_server
        
        self.clock = 0
        self.trace_list = []
        
        
    def starting_state(self):

        # State variables declaration
        self.state = dict()
        self.state['Normal Queue'] = 0
        self.state['Special Queue'] = 0
        self.state['Normal CallBack Queue'] = 0
        self.state['Special CallBack Queue'] = 0
        self.state['Expert Server Status'] = 0
        self.state['Amateur Server Status'] = 0
        self.state['Technical Server Status'] = 0
        self.state['Special Technical Queue'] = 0
        self.state['Normal Technical Queue'] = 0
        self.state['Shift Status'] = 0

        # Data: will save every essential data
        self.data = dict()
        self.data['Users'] = dict()
        """ 
        Users dictionary is implemented to track each customer's entrance time, service start time, and service end time, 
        service technical start time, and service technical end time, for instance:{1:[22, 25, 29, null, null]}. It is
        noteworthy to mention that not all the users use technical service so the 4th and 5th elements of each list is set
        to null for initialization.
        """

        # The dictionary below is needed to store the last time for which each queue has changed in length.
        self.data['Last Time Queue Length Changed'] = dict()
        self.data['Last Time Queue Length Changed']['Normal Queue'] = 0
        self.data['Last Time Queue Length Changed']['Special Queue'] = 0
        self.data['Last Time Queue Length Changed']['Normal CallBack Queue'] = 0
        self.data['Last Time Queue Length Changed']['Special CallBack Queue'] = 0
        self.data['Last Time Queue Length Changed']['Normal Technical Queue'] = 0
        self.data['Last Time Queue Length Changed']['Special Technical Queue'] = 0

        # The dictionary below is needed to store all users' data in each queue
        self.data['Queue Users'] = dict()
        self.data['Queue Users']['Normal Queue'] = dict()
        self.data['Queue Users']['Special Queue'] = dict()
        self.data['Queue Users']['Normal CallBack Queue'] = dict()
        self.data['Queue Users']['Special CallBack Queue'] = dict()
        self.data['Queue Users']['Normal Technical Queue'] = dict()
        self.data['Queue Users']['Special Technical Queue'] = dict()

        # The dictionary below is needed to store the last length of each queue.
        self.data['Last Queue Length'] = dict()
        self.data['Last Queue Length']['Normal Queue'] = 0
        self.data['Last Queue Length']['Special Queue'] = 0
        self.data['Last Queue Length']['Normal CallBack Queue'] = 0
        self.data['Last Queue Length']['Special CallBack Queue'] = 0
        self.data['Last Queue Length']['Normal Technical Queue'] = 0
        self.data['Last Queue Length']['Special Technical Queue'] = 0

        # The dictionary below is needed to store the last time for which each server status has been changed.
        self.data['Last Time Server Status Changed'] = dict()
        self.data['Last Time Server Status Changed']['Expert'] = 0
        self.data['Last Time Server Status Changed']['Amateur'] = 0
        self.data['Last Time Server Status Changed']['Technical'] = 0

        # The dictionary below is needed to store the last server status.
        self.data['Last Server Status'] = dict()
        self.data['Last Server Status']['Expert'] = 0
        self.data['Last Server Status']['Amateur'] = 0
        self.data['Last Server Status']['Technical'] = 0

        # These crumb data are stored for the purpose that is obviously expressed.
        self.data['Last Time Disruption start'] = -1440
        self.data['Number Of No Waiting Special User'] = 0
        self.data['Users To waiting In Technical Queue'] = []
        self.data['Number of special users'] = 0

        # The dictionary below is needed to store the maximum length of each queue during the simulation.
        self.data['Maximum Queue Length'] = dict()
        self.data['Maximum Queue Length']['Normal Queue'] = 0
        self.data['Maximum Queue Length']['Special Queue'] = 0
        self.data['Maximum Queue Length']['Normal CallBack Queue'] = 0
        self.data['Maximum Queue Length']['Special CallBack Queue'] = 0
        self.data['Maximum Queue Length']['Normal Technical Queue'] = 0
        self.data['Maximum Queue Length']['Special Technical Queue'] = 0

        # The dictionary below is needed to store the maximum waiting time of users in each queue during the simulation.
        self.data['Maximum Waiting time'] = dict()
        self.data['Maximum Waiting time']['Normal Queue'] = 0
        self.data['Maximum Waiting time']['Special Queue'] = 0
        self.data['Maximum Waiting time']['Normal CallBack Queue'] = 0
        self.data['Maximum Waiting time']['Special CallBack Queue'] = 0
        self.data['Maximum Waiting time']['Normal Technical Queue'] = 0
        self.data['Maximum Waiting time']['Special Technical Queue'] = 0

        # Cumulative statistics that are necessary to assess the system performance measures.
        self.data['Cumulative Stats'] = dict()
        self.data['Cumulative Stats']['Special Users System Duration time'] = 0
        self.data['Cumulative Stats']['Number of Special Users with no Delay'] = 0
        self.data['Cumulative Stats']['Number of Special Users'] = 0

        # This specific dictionary in cumulative stats is assigned to store area under each queue length curve.
        self.data['Cumulative Stats']['Area Under Queue Length Curve'] = dict()
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Normal Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Special Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Normal CallBack Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Special CallBack Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Normal Technical Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Special Technical Queue'] = 0

        # This specific dictionary in cumulative stats is assigned to store area under waiting time for users in each queue.
        self.data['Cumulative Stats']['Area Under Waiting time'] = dict()
        self.data['Cumulative Stats']['Area Under Waiting time']['Normal Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Special Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Normal CallBack Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Special CallBack Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Normal Technical Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Special Technical Queue'] = 0

        # This specific dictionary in cumulative stats is assigned to store area under each server busy time.
        self.data['Cumulative Stats']['Area Under Server Busy time'] = dict()
        self.data['Cumulative Stats']['Area Under Server Busy time']['Amateur'] = 0
        self.data['Cumulative Stats']['Area Under Server Busy time']['Expert'] = 0
        self.data['Cumulative Stats']['Area Under Server Busy time']['Technical'] = 0

        # FEL initialization, and Starting events that initialize the simulation
        self.future_event_list = list()
        self.future_event_list.append({'Event Type': 'Shift Start/End', 'Event Time': 0, 'User': ''})
        self.future_event_list.append({'Event Type': 'Disruption Start', 'Event Time': 0, 'User': ''})
        self.future_event_list.append({'Event Type': 'Month Change', 'Event Time': 0, 'User': ''})

        if random.random() > self.param_special_porportion:
            self.future_event_list.append({'Event Type': 'Call Start', 'Event Time': 0, 'User': [1, 'Normal', 'Amateur', 0]})
        else:
            self.future_event_list.append({'Event Type': 'Call Start', 'Event Time': 0, 'User': [1, 'Special', 'Expert', 0]})

        return self.state, self.future_event_list, self.data



    def fel_maker(self, event_type: str, user: list, disruption: str = 'No'):
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

        if event_type == 'Call Start':
            if disruption == 'No':  # if the system is not in the disruption condition ...
                event_time = self.clock + self.exponential(self.inter_arrival_param[self.state['Shift Status']])
            else:
                event_time = self.clock + self.exponential(self.disruption_inter_arrival_param[self.state['Shift Status']])

        elif event_type == 'Call End':
            event_time = self.clock + self.exponential(self.service_time_param[user[2]])

        elif event_type == 'Technical Call End':
            event_time = self.clock + self.exponential(self.technical_service_time_param)

        elif event_type == 'Disruption Start':
            event_time = self.clock + 1440 * random.randint(1, 30)

        elif event_type == 'Month Change':
            event_time = self.clock + 30 * 1440

        elif event_type == 'Queue Quit':
            if user[1] == 'Normal':  # if a normal user want to quit from his/her queue ...
                event_time = self.clock + self.uniform(5, max(25, self.state['Normal Queue']))
            else:
                event_time = self.clock + self.uniform(5, max(25, self.state['Special Queue']))

        elif event_type == 'Shift Start/End':
            event_time = self.clock + 480

        new_event = {'Event Type': event_type, 'Event Time': event_time, 'User': user}
        self.future_event_list.append(new_event)



    def exponential(self, beta: float) -> float:
        """
        param lambda_param: mean parameter of exponential distribution
        return: random variate that conforms to exponential distribution
        """
        r = random.random()
        return -beta * math.log(r)



    def uniform(self, a: float, b: float) -> float:
        """
        param a: lower bound for uniform dist.
        param b: upper bound for uniform dist.
        return: random variate that obey uniform dist.
        """
        r = random.random()
        return a + (b - a) * r



    def discrete_uniform(self, a: int, b: int) -> int:
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



    def data_server_calculater(self, name: str):
        """
        This function is supposed to calculate area under each server busy time.
        param data: the dictionary that store every essential data
        param name: each server name, whether is expert, amateur or technical
        """
        self.data['Cumulative Stats']['Area Under Server Busy time'][name] += self.state['{} Server Status'.format(name)] \
                                                                * (self.clock - self.data['Last Time Server Status Changed'][name])
        self.data['Last Time Server Status Changed'][name] = self.clock



    def data_queue_calculater(self, name: str, temp = 0):
        """
        This function is supposed to calculate area under each queue length curve,
        and also the maximum queue length.
        """
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['{} Queue'.format(name)] += (self.state['{} Queue'.format(name)] - temp) \
                                                    * (self.clock - self.data['Last Time Queue Length Changed']['{} Queue'.format(name)])
        self.data['Last Time Queue Length Changed']['{} Queue'.format(name)] = self.clock
        self.data['Maximum Queue Length']['{} Queue'.format(name)] = max(self.data['Maximum Queue Length']['{} Queue'.format(name)],
                                                                    (self.state['{} Queue'.format(name)] - temp +1))



    def data_queue_user(self, name: str, status='', technically='No', has_CallBack='No'):
        parameter = {"No": 1, "Yes": 3}  # to store clock in right position

        if status != 'Exit':
            first_user_in_queue = min(self.data['Queue Users']['{} Queue'.format(name)],
                                          key=self.data['Queue Users']['{} Queue'.format(name)].get)
            potential = self.data['Queue Users']['{} Queue'.format(name)][first_user_in_queue][1]
            self.data['Users'][first_user_in_queue][parameter[technically]] = self.clock
            self.data['Queue Users']['{} Queue'.format(name)].pop(first_user_in_queue, None)

            if has_CallBack == 'Yes':
                self.data['Users'][first_user_in_queue][6] = "it_is_CallBack"
            return first_user_in_queue, potential

        else:
            self.data['Users'][self.user[0]][1] = status
            self.data['Queue Users']['{} Queue'.format(name)].pop(self.user[0], None)



    def call_start(self):
        """
        This function is supposed to implement call start event that is fully described in project's report.
        """
        self.data['Users'][self.user[0]] = [self.clock,     -1,           -1,         None,     None,  self.user[1],   None,          None    ]  # -1 means that the user did not served
                                            # arrival ,start service, end service, start tech, end tech, type user, has call_back, type service

        if self.user[1] == 'Normal':  # if a normal user call ...
            if self.state['Amateur Server Status'] == self.param_numbeer_of_amateur_server:  # if all amateur server are busy ...
                if self.state['Expert Server Status'] < 2:  # if at least one expert server is free ...
                    self.data['Last Server Status']['Expert'] = self.state['Expert Server Status']
                    self.data_server_calculater('Expert')
                    self.state['Expert Server Status'] += 1
                    self.user[2] = 'Expert'
                    self.data['Users'][self.user[0]][1] = self.clock
                    self.fel_maker('Call End', [self.user[0], 'Normal', 'Expert', 0])

                else:  # if all expert servers are also busy at the time ...
                    Temp = "No_CallBack"
                    self.data['Last Queue Length']['Normal Queue'] = self.state['Normal Queue']
                    self.state['Normal Queue'] += 1
                    self.data['Queue Users']['Normal Queue'][self.user[0]] = [self.clock, 0]

                    if self.state['Normal Queue'] > (4 + 1):  # if normal queue length is more than 4 ...
                        if random.random() <= self.param_callback_ratio:  # according to historical data half of users will choose to use call-back option
                            self.data['Last Queue Length']['Normal Queue'] = self.state['Normal Queue']
                            self.state['Normal Queue'] -= 1
                            self.data['Queue Users']['Normal Queue'].pop(self.user[0], None)
                            self.data['Last Queue Length']['Normal Queue'] = self.state['Normal CallBack Queue']
                            self.state['Normal CallBack Queue'] += 1
                            self.data['Queue Users']['Normal CallBack Queue'][self.user[0]] = [self.clock, 0]
                            Temp = "CallBack"

                        else:  # users that did not use call-back option
                            if random.random() <= 0.15:  # according to historical data, 15% of them will choose to quit after some time
                                self.data['Queue Users']['Normal Queue'][self.user[0]] = [self.clock, 1]
                                self.fel_maker('Queue Quit', self.user)

                    if Temp == "CallBack":  # If user would like to use Call-back option
                        self.data_queue_calculater('Normal CallBack', temp=1)

                    elif Temp == "No_CallBack":  # If user do not want to use Call-back option
                        self.data_queue_calculater('Normal', temp=1)

            else:  # if at least one amateur server is free ...
                self.data['Last Server Status']['Amateur'] = self.state['Amateur Server Status']
                self.data_server_calculater('Amateur')
                self.state['Amateur Server Status'] += 1
                self.user[2] = 'Amateur'
                self.data['Users'][self.user[0]][1] = self.clock
                self.fel_maker('Call End', [self.user[0], 'Normal', 'Amateur', 0])

        else:  # if a special user call ...
            self.data['Number of special users'] += 1
            if self.state['Expert Server Status'] < 2:  # if at least one expert server is free ...
                self.data['Last Server Status']['Expert'] = self.state['Expert Server Status']
                self.data_server_calculater('Expert')
                self.state['Expert Server Status'] += 1
                self.user[2] = 'Expert'
                self.data['Users'][self.user[0]][1] = self.clock
                self.data['Number Of No Waiting Special User'] += 1
                self.fel_maker('Call End', [self.user[0], 'Special', 'Expert', 0])

            else:  # if all expert servers are busy ...
                self.data['Last Queue Length']['Special Queue'] = self.state['Special Queue']
                Temp = "No_CallBack"
                self.state['Special Queue'] += 1
                self.data['Queue Users']['Special Queue'][self.user[0]] = [self.clock, 0]

                if self.state['Special Queue'] > (4 + 1):  # if special queue length is more than 4 ...
                    if random.random() <= self.param_callback_ratio:  # according to historical data half of users will choose to use call-back option
                        self.data['Last Queue Length']['Special Queue'] = self.state['Special Queue']
                        self.state['Special Queue'] -= 1
                        self.data['Queue Users']['Special Queue'].pop(self.user[0], None)
                        self.data['Last Queue Length']['Special CallBack Queue'] = self.state['Special CallBack Queue']
                        self.state['Special CallBack Queue'] += 1
                        self.data['Queue Users']['Special CallBack Queue'][self.user[0]] = [self.clock, 0]
                        Temp = "CallBack"

                    else:  # users that did not use call-back option
                        if random.random() <= 0.15:  # according to historical data, 15% of them will choose to quit after some time
                            self.data['Queue Users']['Special Queue'][self.user[0]] = [self.clock, 1]
                            self.fel_maker('Queue Quit', self.user)

                if Temp == "CallBack":  # If user would like to use Call-back option
                    self.data_queue_calculater('Special CallBack', temp=1)

                elif Temp == "No_CallBack":  # If user do not want to use Call-back option
                   self. data_queue_calculater('Special', temp=1)

        new_user = [self.user[0] + 1, '', '', 0]
        if random.random() <= self.param_special_porportion:  # according to data, 30% of users that call this call center are special
            new_user[1] = 'Special'

        else:
            new_user[1] = 'Normal'

        if self.clock >= self.data['Last Time Disruption start'] + 1440:  # whether next user should be scheduled in disruption condition or not
            self.fel_maker('Call Start', new_user, disruption='No')

        else:
            self.fel_maker('Call Start', new_user, disruption='Yes')



    def call_end(self):
        """
        This function is supposed to implement call end event that is fully described in project's report.
        """
        self.data['Users'][self.user[0]][2] = self.clock  # here we store user's call-end time in user's dictionary
        self.data['Users'][self.user[0]][7] = self.user[2] # here we store user's setvice type in user's dictionary

        if random.random() < self.percent_needtechnical :  # according to historical data, 15% of users need technical advice
            if self.state['Technical Server Status'] == 2:  # if all technical users are busy at the time ...
                if self.user[1] == 'Normal':  # if a normal user wants to use technical advice ...
                    self.data['Last Queue Length']['Normal Technical Queue'] = self.state['Normal Technical Queue']
                    self.data_queue_calculater('Normal Technical')
                    self.state['Normal Technical Queue'] += 1
                    self.data['Queue Users']['Normal Technical Queue'][self.user[0]] = [self.clock, 0]
                    self.data['Users To waiting In Technical Queue'].append(self.user[0])

                elif self.user[1] == 'Special':  # if a special user wants to use technical advice ...
                    self.data['Last Queue Length']['Special Technical Queue'] = self.state['Special Technical Queue']
                    self.data_queue_calculater('Special Technical')
                    self.state['Special Technical Queue'] += 1
                    self.data['Queue Users']['Special Technical Queue'][self.user[0]] = [self.clock, 0]
                    self.data['Users To waiting In Technical Queue'].append(self.user[0])

            elif self.state['Technical Server Status'] < 2:  # if at least one technical server is free at the time ...
                self.data['Last Server Status']['Technical'] = self.state['Technical Server Status']
                self.data_server_calculater('Technical')
                self.state['Technical Server Status'] += 1
                self.data['Users'][self.user[0]][3] = self.clock
                self.fel_maker('Technical Call End', self.user)

        if self.user[2] == 'Expert':  # if the server that want to end his/her last call is expert ...
            if self.state['Special Queue'] > 0:  # whether the special queue is empty or not ...
                self.data['Last Queue Length']['Special Queue'] = self.state['Special Queue']
                self.data_queue_calculater('Special')
                self.state['Special Queue'] -= 1
                first_user_in_queue, potential = self.data_queue_user('Special')
                self.fel_maker('Call End', [first_user_in_queue, 'Special', 'Expert', potential])

            else:  # if there is at least one person in the special queue ...
                if self.state['Normal Queue'] == 0:  # if normal user's queue is empty ...
                    if (self.state['Shift Status'] == 2) or (
                            self.state['Shift Status'] == 3):  # if we are in 2nd or 3rd shift of a day
                        if self.state['Special CallBack Queue'] > 0:  # if special user's call-back queue is not empty ...
                            self.data['Last Queue Length']['Special CallBack Queue'] = self.state['Special CallBack Queue']
                            self.data_queue_calculater('Special CallBack')
                            self.state['Special CallBack Queue'] -= 1
                            first_user_in_queue, potential = self.data_queue_user('Special CallBack', has_CallBack= "Yes")
                            self.fel_maker('Call End', [first_user_in_queue, "Special", 'Expert', potential])

                        else:  # if special user's call-back queue is empty ...
                            if self.state['Normal CallBack Queue'] > 0:  # whether normal user's call-back queue is not empty ...
                                self.data['Last Queue Length']['Normal CallBack Queue'] = self.state['Normal CallBack Queue']
                                self.data_queue_calculater('Normal CallBack')
                                self.state['Normal CallBack Queue'] -= 1
                                first_user_in_queue, potential = self.data_queue_user('Normal CallBack', has_CallBack= "Yes")
                                self.fel_maker('Call End', [first_user_in_queue, "Normal", 'Expert', potential])

                            else:  # normal user's call-back queue is empty too ...
                                self.data['Last Server Status']['Expert'] = self.state['Expert Server Status']
                                self.data_server_calculater('Expert')
                                self.state['Expert Server Status'] -= 1

                    else:  # if we are in the 1st shift of the day ...
                        self.data['Last Server Status']['Expert'] = self.state['Expert Server Status']
                        self.data_server_calculater('Expert')
                        self.state['Expert Server Status'] -= 1

                elif self.state['Normal Queue'] > 0:  # whether normal user's queue is not empty ...
                    self.data['Last Queue Length']['Normal Queue'] = self.state['Normal Queue']
                    self.data_queue_calculater('Normal')
                    self.state['Normal Queue'] -= 1
                    first_user_in_queue, potential = self.data_queue_user('Normal')
                    self.fel_maker('Call End', [first_user_in_queue, 'Normal', 'Expert', potential])

        elif self.user[2] == 'Amateur':  # if the server that want to end his/her last call is amateur ...
            if self.state['Normal Queue'] > 0:  # if normal user's queue is not empty ...
                self.data['Last Queue Length']['Normal Queue'] = self.state['Normal Queue']
                self.data_queue_calculater('Normal')
                self.state['Normal Queue'] -= 1
                first_user_in_queue, potential = self.data_queue_user('Normal')
                self.fel_maker('Call End', [first_user_in_queue, 'Normal', 'Amateur', potential])

            elif self.state['Normal Queue'] == 0:  # if normal user's queue is empty ...
                if self.state['Shift Status'] == 2 or self.state['Shift Status'] == 3:  # if we are in 2nd or 3rd shift of a day
                    if self.state['Normal CallBack Queue'] > 0:  # if special user's call-back queue is not empty at the moment ...
                        self.data_queue_calculater('Normal CallBack')
                        self.state['Normal CallBack Queue'] -= 1
                        first_user_in_queue, potential = self.data_queue_user('Normal CallBack', has_CallBack= "Yes")
                        self.data['Users'][first_user_in_queue][1] = self.clock
                        self.fel_maker('Call End', [first_user_in_queue, "Normal", 'Amateur', potential])

                    else:  # if special user's call-back queue is empty at the moment ...
                        self.data['Last Server Status']['Amateur'] = self.state['Amateur Server Status']
                        self.data_server_calculater('Amateur')
                        self.state['Amateur Server Status'] -= 1

                else:  # if we are in 1st shift of a day
                    self.data['Last Server Status']['Amateur'] = self.state['Amateur Server Status']
                    self.data_server_calculater('Amateur')
                    self.state['Amateur Server Status'] -= 1



    def technical_call_end(self):
        """
        This function is supposed to implement technical call end event that is fully described in project's report.
        It is important to mention that technical call start is planned in call end event.
        """
        self.data['Users'][self.user[0]][4] = self.clock  # here we store user's technical call-end time in user's dictionary

        if self.state['Special Technical Queue'] == 0:  # whether there is no special user in the technical queue ...
            if self.state['Normal Technical Queue'] == 0:  # if there is also no normal user in the technical queue ...
                self.data['Last Server Status']['Technical'] = self.state['Technical Server Status']
                self.data_server_calculater('Technical')
                self.state['Technical Server Status'] -= 1

            else:  # if there are at least one normal user in the technical queue ...
                self.data['Last Queue Length']['Normal Technical Queue'] = self.state['Normal Technical Queue']
                self.data_queue_calculater('Normal Technical')
                self.state['Normal Technical Queue'] -= 1
                first_user_in_queue, potential = self.data_queue_user('Normal Technical', technically="Yes")
                self.fel_maker('Technical Call End', [first_user_in_queue, "", "", potential])

        else:  # whether there are at least one special user in the technical queue ...
            self.data['Last Queue Length']['Special Technical Queue'] = self.state['Special Technical Queue']
            self.data_queue_calculater('Special Technical')
            self.state['Special Technical Queue'] -= 1
            first_user_in_queue, potential = self.data_queue_user('Special Technical', technically="Yes")
            self.fel_maker('Technical Call End', [first_user_in_queue, "", "", potential])



    def disruption_start(self):
        """
        This function ganna store last time disruption occurred, and it's defined only to have one function for each event.
        """
        self.data['Last Time Disruption start'] = self.clock



    def month_change(self):
        """
        This function is supposed to implement month change.
        """
        self.fel_maker('Disruption Start', self.user, disruption='Yes')
        self.fel_maker('Month Change', self.user)



    def queue_quit(self):
        """
        This function is supposed to implement queue quit event for users that have potential to do so.
        """
        if self.data['Users'][self.user[0]][1] == -1:  # if it is !=-1 then mean of he start receiving service before quit of queue
            if self.user[1] == 'Normal':
                self.data['Last Queue Length']['Normal Queue'] = self.state['Normal Queue']
                self.data_queue_calculater('Normal')
                self.state['Normal Queue'] -= 1
                self.data_queue_user('Normal', status='Exit')

            else:
                self.data['Number of special users'] -= 1
                self.data['Last Queue Length']['Special Queue'] = self.state['Special Queue']
                self.data_queue_calculater('Special')
                self.state['Special Queue'] -= 1
                self.data_queue_user('Special', status='Exit')



    def shift_start_end(self):
        """
        This function is supposed to implement shift change.
        """
        if self.clock % 1440 < 480:  # if mod(clock, 1440) < 480, this means we are still in first shift
            self.state['Shift Status'] = 1

        elif (self.clock % 1440 >= 480) and (self.clock % 1440 < 960):  # if 480 < mod(clock, 1440) < 960, this means we are in second shift
            self.state['Shift Status'] = 2

        else:
            self.state['Shift Status'] = 3  # if none of the above, so we are in third shift

        self.fel_maker('Shift Start/End', self.user)



    def trace_maker(self):
        """
        This fucntion is supposed to create trace for each current event and append it to the trace list
        """
        trace_data = list(self.state.values())
        trace_data.insert(0, round(self.clock, 3))
        trace_data.insert(0, self.current_event)
        fel_copy = self.sorted_fel.copy()

        while len(fel_copy) > 0:  # Filling trace with events of future event list
            trace_data.append(list(filter(None, fel_copy.pop(0).values())))
        self.trace_list.append(trace_data)



    def simulation(self, trace_creator = False) -> dict:
        """
        This function is meant to do the simulation by help of introduced events.
        param simulation_time: this project is terminating simulation, so this parameter is simulation end time.
        return: data and state dictionary will be returned after one replication is done.
        """
        self.starting_state()
        self.future_event_list.append({'Event Type': 'Shift Start/End', 'Event Time': self.simulation_time, 'User': ''})

        while self.clock < self.simulation_time:
            self.sorted_fel = sorted(self.future_event_list, key=lambda x: x['Event Time'])
            self.current_event = self.sorted_fel[0]  # find imminent event
            self.clock = self.current_event['Event Time']  # advance time to current event time
            self.user = self.current_event['User']  # find the user of that event

            if trace_creator:
                self.trace_maker()

            if self.clock < self.simulation_time:  # the if block below is ganna call proper event function for that event type
                if self.current_event['Event Type'] == 'Call Start':
                    self.call_start()

                elif self.current_event['Event Type'] == 'Call End':
                    self.call_end()

                elif self.current_event['Event Type'] == 'Technical Call End':
                    self.technical_call_end()

                elif self.current_event['Event Type'] == 'Disruption Start':
                    self.disruption_start()

                elif self.current_event['Event Type'] == 'Month Change':
                    self.month_change()

                elif self.current_event['Event Type'] == 'Queue Quit':
                    self.queue_quit()

                elif self.current_event['Event Type'] == 'Shift Start/End':
                    self.shift_start_end()

                self.future_event_list.remove(self.current_event)

            else:  # if simulation time is passed after simulation end time, so FEL must be cleared
                self.future_event_list.clear()

            if trace_creator:
                self.trace_maker()

        return self.data, self.state, self.trace_list



    def calculate_kpi(self) -> dict:
        """
        This function is meant to calculate all KPIs that described in project's report, then it stored them all
        in a dictionary called kpi_results
        return: kpi_results
        """
        self.setter()
        data, state, trace_list = self.simulation()
        cumulative = {"Amateur": 0, "Expert": 0, "Technical": 0}

        kpi_results = dict()

        # In order to find number of peolpe in each queue
        kpi_results['Numbers'] = {}
        kpi_results['Numbers']['Special Queue'] = 0
        kpi_results['Numbers']['Normal Queue'] = 0
        kpi_results['Numbers']['Special Technical Queue'] = 0
        kpi_results['Numbers']['Normal Technical Queue'] = 0
        kpi_results['Numbers']['Special CallBack Queue'] = 0
        kpi_results['Numbers']['Normal CallBack Queue'] = 0

        # Maximum number of people in each queue
        kpi_results['Max Queue Time'] = {}
        kpi_results['Max Queue Time']['Special Technical Queue'] = 0
        kpi_results['Max Queue Time']['Special Queue'] = 0
        kpi_results['Max Queue Time']['Normal Technical Queue'] = 0
        kpi_results['Max Queue Time']['Normal Queue'] = 0
        kpi_results['Max Queue Time']['Special CallBack Queue'] = 0
        kpi_results['Max Queue Time']['Normal CallBack Queue'] = 0

        # Area under queue time curve
        kpi_results['Average Queue Time'] = {}
        kpi_results['Average Queue Time']['Special Queue'] = 0
        kpi_results['Average Queue Time']['Normal Queue'] = 0
        kpi_results['Average Queue Time']['Special Technical Queue'] = 0
        kpi_results['Average Queue Time']['Normal Technical Queue'] = 0
        kpi_results['Average Queue Time']['Special CallBack Queue'] = 0
        kpi_results['Average Queue Time']['Normal CallBack Queue'] = 0

        for i in data['Users'].keys():  # for each user:
            if (data['Users'][i][2] != -1) and (data['Users'][i][1] != -1) and (data['Users'][i][1] != "Exit"):  # Which he/she served in the system
                if data['Users'][i][7] == "Amateur":  # If the user is amateur ...
                    cumulative["Amateur"] += data['Users'][i][2] - data['Users'][i][1]

                else:
                    cumulative["Expert"] += data['Users'][i][2] - data['Users'][i][1]

                if data['Users'][i][5] == "Special":  # If the user is special ...
                    if data['Users'][i][6] is None:
                        kpi_results['Average Queue Time']['Special Queue'] += data['Users'][i][1] - data['Users'][i][0]
                        kpi_results['Numbers']['Special Queue'] += 1
                        kpi_results['Max Queue Time']['Special Queue'] = \
                                            max(kpi_results['Max Queue Time']['Special Queue'], (data['Users'][i][1] - data['Users'][i][0]))

                    elif data['Users'][i][6] == 'it_is_CallBack':
                        kpi_results['Average Queue Time']['Special CallBack Queue'] += data['Users'][i][1] - \
                                                                                              data['Users'][i][0]
                        kpi_results['Numbers']['Special CallBack Queue'] += 1
                        kpi_results['Max Queue Time']['Special CallBack Queue'] = \
                                                max(kpi_results['Max Queue Time']['Special CallBack Queue'], (data['Users'][i][1] - data['Users'][i][0]))

                    if (data['Users'][i][3] is not None) and (data['Users'][i][4] is not None):
                        kpi_results['Numbers']['Special Technical Queue'] += 1
                        kpi_results['Average Queue Time']['Special Technical Queue'] += data['Users'][i][3] - data['Users'][i][2]
                        kpi_results['Max Queue Time']['Special Technical Queue'] = \
                                                max(kpi_results['Max Queue Time']['Special Technical Queue'], (data['Users'][i][3] - data['Users'][i][2]))
                        cumulative["Technical"] += data['Users'][i][4] - data['Users'][i][3]

                if data['Users'][i][5] == "Normal":
                    if data['Users'][i][6] is None:
                        kpi_results['Average Queue Time']['Normal Queue'] += data['Users'][i][1] - data['Users'][i][0]
                        kpi_results['Numbers']['Normal Queue'] += 1
                        kpi_results['Max Queue Time']['Normal Queue'] = \
                                                max(kpi_results['Max Queue Time']['Normal Queue'], (data['Users'][i][1] - data['Users'][i][0]))

                    elif data['Users'][i][6] == 'it_is_CallBack':
                        kpi_results['Average Queue Time']['Normal CallBack Queue'] += data['Users'][i][1] - data['Users'][i][0]
                        kpi_results['Numbers']['Normal CallBack Queue'] += 1
                        kpi_results['Max Queue Time']['Normal CallBack Queue'] = \
                                                max(kpi_results['Max Queue Time']['Normal CallBack Queue'], (data['Users'][i][1] - data['Users'][i][0]))

                    if (data['Users'][i][3] is not None) and (data['Users'][i][4] is not None):
                        kpi_results['Numbers']['Normal Technical Queue'] += 1
                        kpi_results['Average Queue Time']['Normal Technical Queue'] += data['Users'][i][3] - data['Users'][i][2]
                        kpi_results['Max Queue Time']['Normal Technical Queue'] = \
                                                max(kpi_results['Max Queue Time']['Normal Technical Queue'], (data['Users'][i][3] - data['Users'][i][2]))
                        cumulative["Technical"] += data['Users'][i][4] - data['Users'][i][3]

        kpi_results['Average Queue Time']['Special Queue'] = kpi_results['Average Queue Time']['Special Queue'] / \
                                                              kpi_results['Numbers']['Special Queue']
        kpi_results['Average Queue Time']['Normal Queue'] = kpi_results['Average Queue Time']['Normal Queue'] / \
                                                            kpi_results['Numbers']['Normal Queue']
        kpi_results['Average Queue Time']['Special Technical Queue'] = kpi_results['Average Queue Time']['Special Technical Queue'] / \
                                                                        kpi_results['Numbers']['Special Technical Queue']
        kpi_results['Average Queue Time']['Normal Technical Queue'] = kpi_results['Average Queue Time']['Normal Technical Queue'] / \
                                                                      kpi_results['Numbers']['Normal Technical Queue']
        kpi_results['Average Queue Time']['Special CallBack Queue'] = kpi_results['Average Queue Time']['Special CallBack Queue'] / \
                                                                      kpi_results['Numbers']['Special CallBack Queue']
        kpi_results['Average Queue Time']['Normal CallBack Queue'] = kpi_results['Average Queue Time']['Normal CallBack Queue'] / \
                                                                      kpi_results['Numbers']['Normal CallBack Queue']

        server_number = {"Amateur": self.param_numbeer_of_amateur_server, "Expert": 2, "Technical": 2}
        kpi_results['Special Users time in system duration'] = 0
        kpi_results['number of Special Users in system with no waiting'] = 0

        for i in data['Users'].keys():
            if (data['Users'][i][2] != -1) and (data['Users'][i][1] != -1) and (data['Users'][i][1] != "Exit"):
                if (data['Users'][i][5] == "Special") and(data['Users'][i][6] is None ):
                    if (data['Users'][i][3] is None) and (data['Users'][i][4] is None):
                        kpi_results['Special Users time in system duration'] += data['Users'][i][2] - data['Users'][i][0]

                        if (data['Users'][i][1] - data['Users'][i][0]) == 0:
                            kpi_results['number of Special Users in system with no waiting'] += 1

                    elif (data['Users'][i][3] is not None) and (data['Users'][i][4] is not None):
                        kpi_results['Special Users time in system duration'] += data['Users'][i][4] - data['Users'][i][0]

                        if (data['Users'][i][3] - data['Users'][i][2] == 0) and (
                                data['Users'][i][1] - data['Users'][i][0] == 0):
                            kpi_results['number of Special Users in system with no waiting'] += 1

        kpi_results['Special Users time in system duration'] = kpi_results['Special Users time in system duration'] / \
                        (kpi_results['Numbers']['Special Queue'])
        kpi_results['number of Special Users in system with no waiting'] = kpi_results['number of Special Users in system with no waiting'] / \
                        (kpi_results['Numbers']['Special Queue'])
        kpi_results['Average Queue Length'] = {}

        for i in data['Cumulative Stats']['Area Under Queue Length Curve'].keys():
            kpi_results['Average Queue Length'][i] = data['Cumulative Stats']['Area Under Queue Length Curve'][i] / self.simulation_time
        kpi_results['Max Queue Length'] = {}

        for i in data['Maximum Queue Length'].keys():
            kpi_results['Max Queue Length'][i] = data['Maximum Queue Length'][i]
        kpi_results['Server Utilization'] = {}

        for i in data['Cumulative Stats']['Area Under Server Busy time'].keys():
            kpi_results['Server Utilization'][i] = cumulative[i] / (self.simulation_time * server_number[i])

        return kpi_results



    def trace_excel_maker(self):
        """
        This function is only meant to create a trace excel
        """
        trace = pd.DataFrame(self.trace_list)

        columns = list(self.state.keys())  # list of excel columns headers
        columns.insert(0, 'Clock')
        columns.insert(1, 'Current Event')
        columns.extend([f'fel{i}' for i in range(1, trace.shape[1] - 11)])  # to add future event list to trace dataframe
        trace = pd.DataFrame(self.trace_list, columns=columns)
        trace.to_excel('C:/Users/Lenovo/Desktop/trace_dataframe.xlsx', engine='xlsxwriter')



    def calculate_kpi_estimation(self, replication=25, alpha=0.05) -> dict:
        """
        Parameters
        ----------
        replication : int
            Number of independent replication.
        alpha : TYPE, optional
            Type one error. The default is 0.05.

        Returns
        -------
        kpi_result_estimation : dict
            A dictionary that contains all KPI estimations. Each KPI has a list of 3
            numbers in this dictionary; first one is KPI's mean value, second and third
            one are KPI lower and upper bound respectively
        """

        def data_structure():
            return {'Average Queue Length': {'Normal Queue': [],
                                                        'Special Queue': [],
                                                        'Normal CallBack Queue': [],
                                                        'Special CallBack Queue': [],
                                                        'Normal Technical Queue': [],
                                                        'Special Technical Queue': []},
                                'Max Queue Length': {'Normal Queue': [],
                                                    'Special Queue': [],
                                                    'Normal CallBack Queue': [],
                                                    'Special CallBack Queue': [],
                                                    'Normal Technical Queue': [],
                                                    'Special Technical Queue': []},
                                'Average Queue Time': {'Normal Queue': [],
                                                      'Special Queue': [],
                                                      'Normal CallBack Queue': [],
                                                      'Special CallBack Queue': [],
                                                      'Normal Technical Queue': [],
                                                      'Special Technical Queue': []},
                                'Max Queue Time': {'Normal Queue': [],
                                                  'Special Queue': [],
                                                  'Normal CallBack Queue': [],
                                                  'Special CallBack Queue': [],
                                                  'Normal Technical Queue': [],
                                                  'Special Technical Queue': []},
                                'Server Utilization': {'Amateur': [], 'Expert': [], 'Technical': []},
                                'Special Users time in system duration': [],
                                'Number of Special users in system with no waiting': []}
        kpi_result_data = data_structure()
        kpi_result_estimation = data_structure()


        for r in range(replication):
            kpi_result = self.calculate_kpi()

            for i in kpi_result_data.keys():
                if (kpi_result_data[i] != 'Special Users time in system duration') and (kpi_result_data[i] != 'Number of Special users in system with no waiting'):
                    for j in kpi_result_data[i]:
                        kpi_result_data[i][j].append(kpi_result[i][j])

                else:
                    kpi_result_data[i].append(kpi_result[i])

        for i in kpi_result_data.keys():
            if (kpi_result_data[i] != 'Special Users time in system duration') and (kpi_result_data[i] != 'Number of Special users in system with no waiting'):
                for j in kpi_result_data[i]:
                    kpi_result_estimation[i][j].append(np.mean(kpi_result_data[i][j]))
                    kpi_result_estimation[i][j].append(np.mean(kpi_result_data[i][j]) - np.std(kpi_result_data[i][j]) / replication * stats.t.ppf(1 - alpha / 2, replication - 1))
                    kpi_result_estimation[i][j].append(np.mean(kpi_result_data[i][j]) + np.std(kpi_result_data[i][j]) / replication * stats.t.ppf(1 - alpha / 2, replication - 1))

            else:
                kpi_result_estimation[i].append(np.mean(kpi_result_data[i]))
                kpi_result_estimation[i].append(np.mean(kpi_result_data[i]) - np.std(kpi_result_data[i]) / replication * stats.t.ppf(1 - alpha / 2, replication - 1))
                kpi_result_estimation[i].append(np.mean(kpi_result_data[i]) + np.std(kpi_result_data[i]) / replication * stats.t.ppf(1 - alpha / 2, replication - 1))

        return kpi_result_estimation


    def ploting(self,x, y, x_label = "inter_arrival_param", title = 'Normal Queue'):
        plt.figure(figsize=(3,2))   
        plt.plot(x,y,alpha=0.4)
        z = np.polyfit(x, y, 4)
        p = np.poly1d(z)
        plt.plot(x,p(x),'--')
        plt.title(title, size=14)
        error = [np.std(y) for i in range(len(x))]
        z1 = np.polyfit(x, error, 8)
        p1= np.poly1d(z1)
        plt.fill_between(x, (p(x)-p1(x)/2), (p(x)+p1(x)/2),alpha=0.2)
        plt.xlabel(x_label) 
        plt.show()


    def sensitivity_analysis(self,Sensitivity_Variable = 'inter_arrival_param'):

        if Sensitivity_Variable == 'inter_arrival_param':
            x,y1,y2,y3 = {1:[],2:[],3:[]},{1:[],2:[],3:[]},{1:[],2:[],3:[]},{1:[],2:[],3:[]}
            for i in range(1,4):

                for j in range(0,10):

                    self.inter_arrival_param[i] = j * 0.4
                    kpi_result_estimation = self.calculate_kpi_estimation()
                    x[i].append(j * 0.4)
                    y1[i].append(kpi_result_estimation['Average Queue Length']['Normal Queue'][0])
                    y2[i].append(kpi_result_estimation['Average Queue Length']['Normal Technical Queue'][0])
                    y3[i].append(kpi_result_estimation['Average Queue Time']['Special Queue'][0])
                self.ploting(x[i], y1[i],'inter_arrival_param in shift of {}'.format(i),'Normal Queue')
                self.ploting(x[i], y2[i], 'inter_arrival_param in shift of {}'.format(i),'Normal Technical Queue')
                self.ploting(x[i], y3[i],'inter_arrival_param in shift of {}'.format(i),'Special Queue')

        elif Sensitivity_Variable == 'service_time_param':
            x,y1,y2,y3 = {1:[],2:[]},{1:[],2:[]},{1:[],2:[]},{1:[],2:[]}
            for i in range(1,3):

                for j in range(0,10):    
                    self.service_time_param[i] = j 
                    kpi_result_estimation = self.calculate_kpi_estimation()
                    x[i].append(j)
                    y1[i].append(kpi_result_estimation['Average Queue Length']['Normal Queue'][0])
                    y2[i].append(kpi_result_estimation['Average Queue Length']['Normal Technical Queue'][0])
                    y3[i].append(kpi_result_estimation['Average Queue Time']['Special Queue'][0])
                self.ploting(x[i], y1[i],'Average Queue Length in shift of {}'.format(i),'Normal Queue')
                self.ploting(x[i], y2[i], 'Average Queue Length in shift of {}'.format(i),'Normal Technical Queue')
                self.ploting(x[i], y3[i],'Average Queue Length in shift of {}'.format(i),'Special Queue')

        elif Sensitivity_Variable == 'service_time_technical':
            x,y1,y2,y3 = [],[],[],[]
            for j in range(0,15):    
                self.service_time_technical = j 
                kpi_result_estimation = self.calculate_kpi_estimation()
                x.append(j)
                y1.append(kpi_result_estimation['Average Queue Length']['Normal Queue'][0])
                y2.append(kpi_result_estimation['Average Queue Length']['Normal Technical Queue'][0])
                y3.append(kpi_result_estimation['Average Queue Time']['Special Queue'][0])
            self.ploting(x, y1,'service_time_technical','Normal Queue')
            self.ploting(x, y2,'service_time_technical','Normal Technical Queue')
            self.ploting(x, y3,'service_time_technical','Special Queue')
        elif Sensitivity_Variable == 'percent_needtechnical':
            x,y1,y2,y3 = [],[],[],[]
            for j in range(0,7):    
                self.percent_needtechnical = j / 15
                kpi_result_estimation = self.calculate_kpi_estimation()
                x.append(j/15)
                y1.append(kpi_result_estimation['Average Queue Length']['Normal Queue'][0])
                y2.append(kpi_result_estimation['Average Queue Length']['Normal Technical Queue'][0])
                y3.append(kpi_result_estimation['Average Queue Time']['Special Queue'][0])
            self.ploting(x, y1,'service_time_technical','Normal Queue')
            self.ploting(x, y2,'service_time_technical','Normal Technical Queue')
            self.ploting(x, y3,'service_time_technical','Special Queue')

    def warm_up(self):
        self.setter(simulation_time = 3*30*24*60)
        data = self.simulation()[0]
        time = np.array([])
        average_queue_each_time = np.array([])
        for i in data['Users'].keys():  # for each user:
            if (data['Users'][i][2] != -1) and (data['Users'][i][1] != -1) and (data['Users'][i][1] != "Exit"):  # Which he/she served in the system
                if data['Users'][i][5] == "Normal":
                    if data['Users'][i][6] is None:
                        time = np.append(time, data['Users'][i][1])
                        try:
                            
                            average_queue_new = ((data['Users'][i][1]-data['Users'][i][0])+ average_queue_each_time[-1]*len(average_queue_each_time))/(len(average_queue_each_time)+1)
                            average_queue_each_time = np.append(average_queue_each_time,
                                                               average_queue_new)
                        except:
                            average_queue_each_time = np.append(average_queue_each_time,
                                                               0)
        self.ploting(time,average_queue_each_time,x_label = "Time(min)", title = 'Average time of Normal Queue')
        time_after_warmup = int(input("please add the T0 for warm up: "))  #########
        self.ploting(time[time_after_warmup:],average_queue_each_time[time_after_warmup:],x_label = "Time(min)", title = 'Average time of Normal Queue')
        
    
System_I = CallCenterSimulation(param_numbeer_of_amateur_server=3, param_callback_ratio=0, param_special_porportion=0.4, 
                                inter_arrival_param={1: 1.1, 2: 1.1, 3: 1.1}, disruption_inter_arrival_param={1: 1.1, 2: 1.1, 3: 1.1},
                                service_time_param={"Amateur": 7, "Expert": 3}, technical_service_time_param=10, percent_needtechnical=0.15,
                                simulation_time=30*24*60)

#result = System_I.calculate_kpi_estimation(replication=25)
System_I.warm_up()

end_time = time.time()
print('Execution time: {}'.format(end_time - start_time))
