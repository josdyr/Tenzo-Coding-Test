import datetime
import sys

def convert_pm_am(time_value):
    if time_value is not None:
        if 'PM' in time_value.upper():
            time_value = time_value.replace('PM', '') # remove PM
            time_value = int(time_value) + 12 # convert time, cast to int
        elif 'AM' in time_value.upper():
            time_value = time_value.replace('AM', '') # remove AM
            time_value = int(time_value) # cast to int

    return time_value

def get_start_end(string_time):
    start_break, end_break = string_time.split("-")
    return start_break, end_break

def get_hour_minute(break_time):
    if ":" in break_time or "." in break_time:
        try:
            break_hour, break_minute = break_time.split(".")
        except Exception as e:
            print("Could not split on '.'", file=sys.stderr)
        try:
            break_hour, break_minute = break_time.split(":")
        except Exception as e:
            print("Could not split on ':'", file=sys.stderr)
    else:
        break_hour = break_time
        break_minute = None

    return convert_pm_am(break_hour), convert_pm_am(break_minute)

import ipdb; ipdb.set_trace(context=11)
string_time = "4-4.10PM"
start_break, end_break = get_start_end(string_time)
start_break_hour, start_break_minute = get_hour_minute(start_break)
end_break_hour, end_break_minute = get_hour_minute(end_break)

start_break_hour, start_break_minute
end_break_hour, end_break_minute
