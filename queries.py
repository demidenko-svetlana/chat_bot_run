from sqlalchemy import text
from database import Event, session


def rus_event(country):
    rus_location = session.query(Event) \
        .filter(Event.country == 'Россия').all()

    for loc in rus_location:
        event_location = loc.event
        return event_location


def b_event(country):
    border_location = session.query(Event) \
        .filter(Event.country != 'Россия').all()

    for b_loc in border_location:
        b_location = b_loc.event
        return b_location


def date_event(date):
    dates = session.query(Event) \
        .filter(Event.date.like(f'%{date}')).all()

    for d_input in dates:
        choosing_dates = d_input.date
        return choosing_dates


def event_date_country(dates, loc):
    ew = session.query(Event) \
        .filter(Event.date.like(f'%{dates}')). \
        filter(Event.country == (loc)).all()
    return ew
