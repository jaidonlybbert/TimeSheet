# Author: Jaidon Lybbert
# Date: July 4, 2019
#
# Design purpsose: a time management tool for recording start and end times for
#   user defined tasks.
#
# Features: Provides a way to keep track of how long is spent on various tasks,
#   and delivers report by request


import datetime

# Check if the user last clocked in, or out
def isClockedIn():
    try:
        with open("status.txt", 'r') as fhand:
            status = fhand.readline()
    except:
        print("No status.txt found: creating one now.\n")
        with open("status.txt", 'w+') as fhand:
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
def clockIn():
    if isClockedIn() == True:
        print("Error: you are already clocked in!")
        return

    time = datetime.datetime.now()
    with open("timeLog.txt", "a+") as fhand:
        fhand.write("IN: %s\n" % time)
    with open("status.txt", "w") as fhand:
        fhand.write("1")


# Clocks user out
def clockOut():
    if isClockedIn() == False:
        print("Error: you are already clocked out!")
        return

    time = datetime.datetime.now()
    with open("timeLog.txt", "a+") as fhand:
        fhand.write("OUT: %s\n" % time)
    with open("status.txt", "w") as fhand:
        fhand.write("0")


# Determines whether to clock user in or out, and does so
def autoClock():
    if isClockedIn():
        clockOut()
    else:
        clockIn()
