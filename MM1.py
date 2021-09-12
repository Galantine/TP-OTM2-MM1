from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
import datetime

def formatTime(hours):    
    delta = datetime.timedelta(hours=hours)  
    return delta - datetime.timedelta(microseconds=delta.microseconds)

class Entry:
    def __init__(self, arrival, serviceTime, serviced, wait):
        self.arrival = 0
        self.serviceTime = 0
        self.serviced = 0
        self.wait = 0

    def toString(self):
        return str(formatTime(self.arrival)) + "       " + str(formatTime(self.serviceTime)) + "       " + str(formatTime(self.serviced)) + "       " + str(formatTime(self.wait))

numServers = 1
simulationTime = 1 # time units
entryRate = 4 # per time unit
serviceRate = 2 # per time unit
qtdEntries = 0 # total number of entries on the queue

for i in range(simulationTime):
    qtdEntries+=int(np.random.poisson(entryRate)) # for each time unit generate number of entries

list = [Entry(0,0,0,0) for i in range(qtdEntries)] # create list with all entries

list[0].serviceTime = np.random.exponential(1/serviceRate) # gives value for the first entry assuming we start "recording"
                                                           # when the first entry comes, so it will start on 0
accumulatedServiceTime = list[0].serviceTime # accumulated service time to know if entries will have to wait or not

queueSizes = []
queueSizes.append(1)

for i in range(1, qtdEntries): # iteration over list to get the values
    list[i].arrival = list[i-1].arrival + np.random.exponential(1/entryRate) # the nth entry will have an arrival time later than the (n-1)th entry
    list[i].serviceTime = np.random.exponential(1/serviceRate) # calc the nth entry's serviceTime
    if list[i].arrival < accumulatedServiceTime: # if the entry arrivals while there are still services to be done
        list[i].serviced = accumulatedServiceTime # the entry will be serviced when and only when all previous ones finish
        accumulatedServiceTime+=list[i].serviceTime # accumulated time will be updated adding the current entry service time to it
    else:                                        # if the entry arrivals when or after all previous services are done
        list[i].serviced = list[i].arrival       # since it arrived when the list is effectively empty it will be serviced when it arrives
        accumulatedServiceTime+=list[i].arrival+list[i].serviceTime # the accumulated time is now updated to be the time when the current entry finishes
    list[i].wait = list[i].serviced - list[i].arrival # how much time the entry waited is now stored

for i in range(qtdEntries):
    print("Arrival       ServiceTime   Serviced       WaitTime")
    print(list[i].toString())
    print("\n")

serviceTimes = [list[i].serviceTime for i in range(len(list))]
print("\nDuração média de uma tarefa: " + str(formatTime(np.average(serviceTimes))))

waitTimes = [list[i].wait for i in range(len(list))]
print("\nTempo de espera médio de uma tarefa: " + str(formatTime(np.average(waitTimes))))

totalAverageServiceTime = [list[i].wait+list[i].serviceTime for i in range(len(list))]
print("\nTempo total médio de uma tarefa: " + str(formatTime(np.average(totalAverageServiceTime))))

input('Press ENTER to exit')