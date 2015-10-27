# Assumption: hotel deals only count towards days during their start date/end date duration,
# even if the user is staying for days outside of that interval.
import sys
import csv
import datetime
import argparse

def parse_date(date_str):
    """
    Returns a datetime.date object
    """
    try:
        year, month, day = int(date_str[:4]), int(date_str[5:7]), int(date_str[8:])
        date = datetime.date(year, month, day)
    except ValueError as e:
        print "Invalid value as date: " + date_str
        print "Date should be in form: yyyy-mm-dd"
        sys.exit()
    return date

def get_deal_duration(deal_start, deal_end, check_in, duration):
    """
    Determines the intersection between deal dates and hotel stay dates.
    Returns the number of days in the intersection.
    """
    deal_start = parse_date(deal_start)
    deal_end = parse_date(deal_end)
    check_in = parse_date(check_in)
    duration = datetime.timedelta(duration)
    check_out = check_in + duration
    if deal_end < check_in or deal_start >= check_out:
        return 0
    elif deal_start < check_in:
        if deal_end < check_out:
            return (deal_end - check_in).days
        else:
            return (check_out - check_in).days
    elif deal_start < check_out:
        if deal_end < check_out:
            return (deal_end - deal_start).days
        else:
            return (check_out - deal_start).days

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to csv file")
    parser.add_argument("hotel", help="hotel to search for best deal")
    parser.add_argument("check_in", help="check in date")
    parser.add_argument("duration", help="duration of stay at hotel", type=int)
    args = parser.parse_args()
    path, hotel, check_in, duration = args.path, args.hotel, args.check_in, args.duration
    csv_file = open(path, "r")

    reader = csv.reader(csv_file)
    header = reader.next()
    best_deal = "no deals available"
    best_price = float('inf')
    for row in reader:
        if row[0] == hotel:
            _, rate, promo, deal_value, deal_type, deal_start, deal_end = row
            rate, deal_value = int(rate), int(deal_value)
            deal_duration = get_deal_duration(deal_start, deal_end, check_in, duration)
            if deal_duration:
                cost = None
                if deal_type == 'rebate' or (deal_type == 'rebate_3plus' and duration >= 3):
                    cost = duration * rate + deal_value
                elif deal_type == 'pct':
                    cost = duration * rate * (1 + float(deal_value)/100)
                if cost and cost < best_price:
                    best_deal, best_price = promo, cost
    print(best_deal)
