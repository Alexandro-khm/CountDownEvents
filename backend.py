import json
import os
from datetime import datetime

JSON_FILENAME = 'events.json'
TELEGRAM_TOKEN = ''

def add_event(event, date, time, event_json=None):
    if event_json is None:
        event_json = []
    event_json.append({
        'event': event,
        'date': date,
        'time': time
    })
    return event_json

# def read_event(event):
#     return event['event'], event['date'], event['time']

def load_events(file):
    if not os.path.exists(file):
        return []
    with open(file) as f:
        events = json.load(f)
    return events

def save_events(file, events):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(events, f)


def sort_events(events):
    def parse_event_datetime(event):
        return datetime.strptime(f"{event['date']} {event['time']}", '%d-%m-%Y %H:%M')

    return sorted(events, key=parse_event_datetime)

def time_to_go(date, time):
    date_time = date + ' ' + time
    date_time_formatted = datetime.strptime(date_time, '%d-%m-%Y %H:%M')
    datetime_now = datetime.now()
    difference_date = date_time_formatted - datetime_now
    days = int(difference_date.days)
    hours = int(difference_date.seconds // 3600)
    minutes = int((difference_date.seconds - (hours * 3600)) // 60)
    seconds = int(difference_date.seconds - (hours * 3600) - (minutes * 60))
    return days, hours, minutes, seconds
