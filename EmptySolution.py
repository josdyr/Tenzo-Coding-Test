"""
Please write you name here: Jostein Dyrseth
"""
import csv
import datetime
import re


def process_shifts(path_to_csv):
    """

    :param path_to_csv: The path to the work_shift.csv
    :type string:
    :return: A dictionary with time as key (string) with format %H:%M
        (e.g. "18:00") and cost as value (Number)
    For example, it should be something like :
    {
        "17:00": 50,
        "22:00: 40,
    }
    In other words, for the hour beginning at 17:00, labour cost was
    50 pounds
    :rtype dict:
    """
    hourly_rate = {hour: 1 for hour in range(24)} # initialise the dictionary

    with open(path_to_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader) # skip header
        for row in reader:
            start = int(row[3][0:2])
            hourly_fraction = None # defaults to only whole hours
            if row[1][3:5] != '00':
                hourly_fraction = int(row[1][3:5]) / 60 # gets the additional fraction of the next hour
            finish = int(row[1][0:2])

            s_break_start, s_break_end = row[0].split("-")
            print(s_break_start, s_break_end)
            import ipdb; ipdb.set_trace(context=11)

            break_fraction = None
            if 'PM' in s_break_start:
                s_break_start = s_break_start.replace('PM', '')
                if '.' in s_break_start or ':' in s_break_start:
                    s_break_start = s_break_start.replace('.', ':')
                    minutes = s_break_start.split(":")[1]
                    if minutes != '00':
                        break_fraction = int(minutes) / 60
                s_break_start = int(s_break_start.split(':')[0]) + 12
            elif 'AM' in s_break_start:
                s_break_start = s_break_start.replace('AM', '')
                if '.' in s_break_start or ':' in s_break_start:
                    s_break_start = s_break_start.replace('.', ':')
                    minutes = s_break_start.split(":")[1]
                    if minutes != '00':
                        break_fraction = int(minutes) / 60
                s_break_start = int(s_break_start.split(':')[0]) - 12

            if 'PM' in s_break_end:
                s_break_end = s_break_end.replace('PM', '')
                if '.' in s_break_end or ':' in s_break_end:
                    s_break_end = s_break_end.replace('.', ':')
                    minutes = s_break_end.split(":")[1]
                    if minutes != '00':
                        break_fraction = int(minutes) / 60
                s_break_end = int(s_break_end.split(':')[0]) + 12
            elif 'AM' in s_break_end:
                s_break_end = s_break_end.replace('AM', '')
                if '.' in s_break_end or ':' in s_break_end:
                    s_break_end = s_break_end.replace('.', ':')
                    minutes = s_break_end.split(":")[1]
                    if minutes != '00':
                        break_fraction = int(minutes) / 60
                s_break_end = int(s_break_end.split(':')[0]) - 12

            print(s_break_start, s_break_end)

            for hour in range(start, finish):
                total_rate = hourly_rate[hour]
                hourly_rate.update({hour: total_rate + float(row[2])})
                if hourly_fraction:
                    hourly_rate.update({hour+1: total_rate + hourly_fraction})

    return hourly_rate


def process_sales(path_to_csv):
    """

    :param path_to_csv: The path to the transactions.csv
    :type string:
    :return: A dictionary with time (string) with format %H:%M as key and
    sales as value (string),
    and corresponding value with format %H:%M (e.g. "18:00"),
    and type float)
    For example, it should be something like :
    {
        "17:00": 250,
        "22:00": 0,
    },
    This means, for the hour beginning at 17:00, the sales were 250 dollars
    and for the hour beginning at 22:00, the sales were 0.

    :rtype dict:
    """
    return

def compute_percentage(shifts, sales):
    """

    :param shifts:
    :type shifts: dict
    :param sales:
    :type sales: dict
    :return: A dictionary with time as key (string) with format %H:%M and
    percentage of labour cost per sales as value (float),
    If the sales are null, then return -cost instead of percentage
    For example, it should be something like :
    {
        "17:00": 20,
        "22:00": -40,
    }
    :rtype: dict
    """
    return

def best_and_worst_hour(percentages):
    """

    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """

    return

def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)
    return best_hour, worst_hour

if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = "transactions.csv"
    path_to_shifts = "work_shifts.csv"
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)


# Please write you name here: Jostein Dyrseth
