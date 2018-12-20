#!/usr/bin/env python
'''
--------------------------------------------------
TIM - Time Is Money
A small time tracker
--------------------------------------------------
'''

import pickle
from sys import argv
from os import getenv
from os.path import join as pjoin
from os.path import exists as file_exists
from os.path import isdir
from datetime import datetime, timedelta

filepath = pjoin(getenv("HOME", "."), ".tim_data")

action_help = {"start": "Start tracking an activity",
               "stop": "Stop an active tracking",
               "reset": "Reset an activity",
               "delete": "Delete an existing activity",
               "stats": "Show statistics on an activity"}


def start_activity(data, activity):
    if activity in data:
        # Check if already started
        if "activation_time" in data[activity]:
            # Already Active
            print("Activity {} is already being monitored. \
                  Quitting.".format(activity))
        else:
            # Start Activity
            data[activity]["activation_time"] = datetime.now()
            data[activity]["last_active"] = datetime.now()
    else:
        # Create new
        data[activity] = {
            "creation_time": datetime.now(),
            "last_active": datetime.now(),
            "activation_time": datetime.now(),
            "elapsed_time": timedelta(0),
            "sessions": []
        }


def stop_activity(data, activity):
    if activity in data:
        # Activity exists
        start_time = data[activity]["activation_time"]
        stop_time = datetime.now()
        delta = stop_time - start_time
        data[activity]["elapsed_time"] += delta
        data[activity]["sessions"].append({
            "date": datetime.today(),
            "elapsed": delta
        })
        del start_time
        del data[activity]["activation_time"]
    else:
        print("Activity {} was not started. Cannot stop a \
              non-started activity".format(activity))
        quit()


def delete_activity(data, activity):
    if activity in data:
        del data[activity]
        print("Activity {} deleted".format(activity))
    else:
        print("Activity {} does not exist".format(activity))
        quit()


def reset_activity(data, activity):
    if activity in data:
        data[activity]["elapsed_time"] = timedelta(0)
        data[activity]["sessions"] = []
        print("Activity {} reset".format(activity))
    else:
        print("Activity {} does not exist".format(activity))
        quit()


def activity_stats(data, activity, detail=True):
    if activity in data:
        print("Name: {}".format(activity))
        status = "Inactive"
        if "activation_time" in data[activity]:
            status = "Active"
        print("Status: {}".format(status))
        print("Elapsed Time: {}".format(data[activity]["elapsed_time"]))
        print("Created on: {}".format(data[activity]["creation_time"]))
        print("Last Activity: {}".format(data[activity]["last_active"]))
        if detail:
            print("Sessions:")
            for session in data[activity]["sessions"]:
                print("Date: {} - Duration: {}".format(session["date"],
                                                       session["elapsed"]))
    else:
        print("Activity {} does not exist".format(activity))
        quit()


actions = {"start": start_activity,
           "stop": stop_activity,
           "reset": reset_activity,
           "delete": delete_activity,
           "stats": activity_stats}


def load_data(filepath):
    data = {}
    if (file_exists(filepath)):
        if (isdir(filepath)):
            print("Error while reading the data file: it is a directory")
            quit()
        with open(filepath, "rb") as fil:
            data = pickle.load(fil)
    return data


def main(action, activity):
    """
    The main function, doing the necessary work to calculate and
    monitor activities

    Keyword Arguments:
    Action - A string representing the action to perform
    Activity - The name of the activity to perform the action on
    """
    data = load_data(filepath)
    actions[action](data, activity)
    with open(filepath, "wb") as fil:
        pickle.dump(data, fil)


def print_program_info():
    """
    Prints the program info
    """
    print("Tim - A simple and bare-bones time tracker")
    print("Version 0.2")
    print("------------------------------------------")


def show_help(action=None):
    """
    Shows a help screen, depending on the option selected

    Keyword Arguments:
    action - The action to show the help line for
    """
    print_program_info()
    if action is None:
        print("tim [{}] activity_name\n".format("|".join(actions.keys())))
        for action in actions.keys():
            print("{} - {}".format(action, action_help[action]))
    else:
        print("{} - {}".format(action, action_help[action]))
    quit()


def show_all_stats():
    data = load_data(filepath)
    if len(data) == 0:
        print("No Statistics to show")
    else:
        for activity in data:
            activity_stats(data, activity, False)
            print("------------------------------")


def parse_args(args):
    """
    Parses command line arguments

    Keyword Arguments:
    args - A copy of sys.argv
    """
    if (len(args) == 1):
        show_help()
    elif (len(args) == 2):
        if (args[1] == "stats"):
            show_all_stats()
        elif (args[1] in actions.keys()):
            show_help(args[1])
        else:
            print("Invalid action selected")
            show_help()
        quit()
    elif (len(args) > 3):
        print("Too Many Arguments")
        show_help()
        quit()
    else:
        return args[1], args[2]


if __name__ == "__main__":
    action, activity = parse_args(argv)
    main(action, activity)

# vi: cc=80
