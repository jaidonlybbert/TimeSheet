# Author: Jaidon Lybbert
# Date: July 4, 2019
#
# Design purpsose: a time management tool for recording start and end times for
#   user defined tasks.
#
# Features: Provides a way to keep track of how long is spent on various tasks,
#   and delivers report by request
# To add: On clockout, display session length


import datetime
from sys import argv

sessionTask = ''
timeLogPath = '/home/jaidon/Documents/Python/TimeSheet/timeLog.txt'
statusPath = '/home/jaidon/Documents/Python/TimeSheet/status.txt'
helpPath = '/home/jaidon/Documents/Python/TimeSheet/status.txt'

def displayStatus():
    if isClockedIn() == False:
        try:
            with open(timeLogPath, 'r') as fhand:
                for line in fhand.readlines():
                    if line[0] == "$" and line[1] == "O":
                        time = line[6:-1]
            print "Clocked out at %s." % time
        except:
            print "New user."
    else:
        with open(timeLogPath, 'r') as fhand:
            for line in fhand.readlines():
                if line[0] == "$" and line[1] == "I":
                    time = line[5:-1]
        print "Clocked In at %s." % time


def secondsToHMS(intervalInSeconds):
    interval = [0, 0, intervalInSeconds]
    interval[0] = (interval[2] / 3600) - ((interval[2] % 3600) / 3600)
    interval[1] = ((interval[2] % 3600) / 60) - ((interval[2] % 3600) % 60) / 60
    interval[2] = interval[2] % 60

    intervalString = '{0:02.0f}:{1:02.0f}:{2:02.0f}'.format(interval[0],
      interval[1], interval[2])

    return intervalString


def calculateIntervals():
    timesOut = []
    timesIn = []
    dateTimesIn = []
    dateTimesOut = []
    intervals = []
    tasks = []
    taskIntervals = {}

    # Load data from log into lists
    with open(timeLogPath, 'r') as fhand:
        lines = fhand.readlines()

        i = 0
        for line in lines:
            if (i == 0):
                pass
            elif (lines[i][0] == '\n'):
                pass
            elif (lines[i][0] == '$' and lines[i - 1][0] == '$'):
                timesOut.append(lines[i][6:-1])
                timesIn.append(lines[i - 1][5:-1])
                tasks.append(lines[i - 2][:-1])
            i += 1

    for i in timesOut:
        dateTimesOut.append(datetime.datetime(int(i[:4]), int(i[5:7]),
          int(i[8:10]), int(i[11:13]), int(i[14:16]), int(i[17:19])))
    for j in timesIn:
        dateTimesIn.append(datetime.datetime(int(j[:4]), int(j[5:7]),
          int(j[8:10]), int(j[11:13]), int(j[14:16]), int(j[17:19])))

    k = 0
    for time in dateTimesIn:
        intervals.append(datetime.timedelta.total_seconds(dateTimesOut[k] - dateTimesIn[k]))
        k += 1

    l = 0
    for task in tasks:
        if task in taskIntervals:
            taskIntervals[task] += intervals[l]
        else:
            taskIntervals[task] = intervals[l]
        l += 1

    for taskInterval in taskIntervals:
        taskIntervals[taskInterval] = secondsToHMS(taskIntervals[taskInterval])

    return taskIntervals


def generateStatistics():
    taskIntervals = calculateIntervals()

    print '{0:30} {1:>15}'.format("Task:", "Time spent:")
    for key, value in taskIntervals.items():
        print '{0:30} {1:>14}s'.format(key, value)


# Display help text
def loadHelp():
    with open(helpPath, 'r') as fhand:
        print fhand.read()


# Prints data and statistics of recorded sessions
def printStats():
    generateStatistics()


# Get current task as argument passed on execution
def loadSession():
    global sessionTask

    try:
        sessionTask = argv[1].lower()
    except:
        print("Missing required argument. Try 'help' for more information.\n")
        exit()

    if (sessionTask == "help"):
        loadHelp()
    elif (sessionTask == "stats"):
        printStats()
    elif (sessionTask == "status"):
        displayStatus()
    else:
        autoClock(sessionTask)


# Check if the user last clocked in, or out
def isClockedIn():
    try:
        with open(statusPath, 'r') as fhand:
            status = fhand.readline()
    except:
        print("No status.txt found: creating one now.\n")
        with open(statusPath, 'w+') as fhand:
            fhand.write("0")
        return False

    if (status == "0"):
        return False
    elif (status == "1"):
        return True
    else:
        print("Fatal error reading status.txt. Exiting.\n")
        exit()


# Clocks user in
def clockIn(sessionTask):
    if isClockedIn() == True:
        print("Error: you are already clocked in!")
        return

    time = datetime.datetime.now()

    with open(timeLogPath, "a+") as fhand:
        fhand.write("%s\n$IN: %s\n" % (sessionTask, time))
    with open(statusPath, "w") as fhand:
        fhand.write("1")

    print("Clocked in: %s" % time)


# Clocks user out
def clockOut():
    if isClockedIn() == False:
        print("Error: you are already clocked out!")
        return

    time = datetime.datetime.now()

    with open(timeLogPath, "a+") as fhand:
        fhand.write("$OUT: %s\n\n" % time)
    with open(statusPath, "w") as fhand:
        fhand.write("0")

    print("Clocked out: %s" % time)


# Determines whether to clock user in or out, and does so
def autoClock(sessionTask):
    if isClockedIn():
        clockOut()
    else:
        clockIn(sessionTask)


# Clears all recorded data
def clearLog():
    try:
        with open(timeLogPath, "w+") as fhand:
            fhand.write('')
    except:
        pass

    print("Log successfully cleared.\n")


def main():
    loadSession()


main()
