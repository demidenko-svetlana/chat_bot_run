from database import Event, session


rus_location = session.query(Event) \
    .filter(Event.country == 'Россия').all()

for loc in rus_location:
    print(f'Забег {loc.event} проводится в России')


border_location = session.query(Event) \
    .filter(Event.country != 'Россия').all()

for b_loc in border_location:
    print(f'Забег {b_loc.event} проводится за границей')


date_input = input()
dates = session.query(Event) \
    .filter(Event.date.like(f'%{date_input}')).all()

for d_input in dates:
    print(f'В указанном вами месяце {date_input} есть забег {d_input.event}')


