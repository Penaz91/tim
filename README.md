TIM - Time is Money
===================

`tim` is a small program dedicated to time tracking.

The main idea behind `tim` is having a time tracking application that doesn't sit in the background, wasting system resources, but instead saving a timestamp and perform the calculations when the activity is stopped. This makes it ideal to be used on command line, inside scripts (maybe that get triggered on `cd`-ing in and out of a directory).

Usage
---------

`tim` Shows the current activity, if none is active, it shows the help screen

`tim start [activity name]` Starts tracking a new activity, if an activity with the same name was started, the time will be added to the existing activity

`tim stop [activity name]` Stops the time tracking and calculates the time between the start command and the stop command

`tim stats [activity name]` Shows the time spent a certain activity (default: show all)

`tim reset [activity name]` Resets the time spent on a certain activity

`tim delete [activity name]` Deletes a certain activity from the activity database
