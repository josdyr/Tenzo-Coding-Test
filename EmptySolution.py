"""
Please write you name here: Jostein Dyrseth
"""
import csv
import datetime
import sys
import pprint


def convert_to_24(time_value, type):
    if time_value is not None:
        if 'PM' in time_value.upper():
            time_value = time_value.replace('PM', '') # remove PM
            if type == 'hour':
                time_value = int(time_value) + 12 # convert to 24-hour format
            else:
                time_value = int(time_value)
        elif 'AM' in time_value.upper():
            time_value = time_value.replace('AM', '') # remove AM
            time_value = int(time_value)
    else:
        time_value = 0

    return time_value


def get_start_end(string_time):
    start_break, end_break = string_time.split("-")
    return start_break, end_break


def get_hour_minute(break_time):
    if ":" in break_time or "." in break_time:
        try:
            break_hour, break_minute = break_time.split(".")
        except Exception as e:
            # print("Could not split on '.'", file=sys.stderr)
            pass
        try:
            break_hour, break_minute = break_time.split(":")
        except Exception as e:
            # print("Could not split on ':'", file=sys.stderr)
            pass
    else:
        break_hour = break_time
        break_minute = None

    break_hour = convert_to_24(break_hour, 'hour')
    break_minute = convert_to_24(break_minute, 'minute')

    if int(break_hour) < 9: # Assuming day-shift starts at 9
        # convert to 24-hour format
        break_hour = int(break_hour) + 12

    return int(break_hour), int(break_minute)


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

    shifts = dict()

    # for each row in file
    with open(path_to_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.__next__() # skip header

        for shift in reader:

            # work shift
            start_shift, end_shift = shift[3], shift[1]
            start_hour = int(start_shift[:2])
            start_minute = int(start_shift[3:])
            end_hour = int(end_shift[:2])
            end_minute = int(end_shift[3:])

            # break
            start_break, end_break = get_start_end(shift[0])
            start_break_hour, start_break_minute = get_hour_minute(start_break)
            end_break_hour, end_break_minute = get_hour_minute(end_break)

            # pay rate
            current_pay_rate = float(shift[2])

            # print('work: {}:{}-{}:{}\tbreak: {}:{}-{}:{}\trate: {}'.format(start_hour, start_minute, end_hour, end_minute, start_break_hour, start_break_minute, end_break_hour, end_break_minute, current_pay_rate))

            for hour in range(start_hour, end_hour+1 if end_minute != 0 else end_hour):

                str_hour = str(hour) + ':00' if hour > 9 else '0' + str(hour) + ':00'
                if str_hour in shifts:
                    hourly_cost = shifts[str_hour] # get hourly_cost
                else:
                    hourly_cost = 0

                # add values to dictionary
                if start_break_hour <= hour < end_break_hour: # skip adding to dictionary
                    if hour == start_break_hour and start_break_minute != 0: # unless additional minutes start
                        # print("Added {} to dict".format(hour))
                        shifts.update({str_hour : hourly_cost + current_pay_rate * (start_break_minute / 60)})
                    else: # skip the break
                        # print("Skipping break-hour: {}".format(hour))
                        pass
                elif hour == end_break_hour and end_break_minute != 0: # unless additional minutes end
                    # print("Added {} to dict".format(hour))
                    shifts.update({str_hour : hourly_cost + current_pay_rate * (abs(end_break_minute - 60) / 60)})
                elif hour == end_hour and end_minute != 0:
                    # print("Added {} to dict".format(hour))
                    shifts.update({str_hour : hourly_cost + current_pay_rate * (end_minute / 60)})
                else:
                    # print("Added {} to dict".format(hour))
                    shifts.update({str_hour : hourly_cost + current_pay_rate})

    return shifts


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

    sales = dict()

    # for each row in file
    with open(path_to_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.__next__() # skip header

        for transaction in reader:
            hour = transaction[1][:2] + ':00' if int(transaction[1][:2]) > 9 else '0' + transaction[1][:2] + ':00'
            amount = float(transaction[0])
            total_sale = 0
            if hour in sales:
                total_sale = sales[hour]
            sales.update({hour : total_sale + amount})

    return sales

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
    percentage_dict = dict()
    for time in sorted(shifts):
        cost = shifts[time]
        try:
            sale = sales[time]
            percentage = cost / sale
        except:
            sale = None
            percentage = cost * (-1)
        percentage_dict.update({time : percentage})

    return percentage_dict

def best_and_worst_hour(percentages):
    """

    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """

    # import ipdb; ipdb.set_trace(context=11)

    best_to_worst_hours = []

    index = 0
    for value in sorted(percentages.values()):
        if value < 0:
            best_to_worst_hours.append(value)
            index += 1
        else: # positive value
            # import ipdb; ipdb.set_trace()
            best_to_worst_hours.insert(index, value)

    best_to_worst_hours = [value for value in reversed(best_to_worst_hours)]
    # print(best_to_worst_hours)
    # print(best_to_worst_hours[0], best_to_worst_hours[-1])

    import ipdb; ipdb.set_trace(context=11)

    # assuming to return a float for both best_hour, worst_hour (from the list) - and not the list itself as the main function expects two values. However the list is prepared if need be.
    return best_to_worst_hours[0], best_to_worst_hours[-1]

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

# I wanted to do TDD if I had more time. This would allow me to test my own code which would be very benefitial.
