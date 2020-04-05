import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm.session import sessionmaker

# флаг echo влючает ведение лога через стандартный модуль logging. Когда он включен, мы видим все созданные SQL-запросы
engine = create_engine('sqlite:///mydb.db', echo=False)

base = declarative_base()

class Event(base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=True)
    decline = Column(String, nullable=True)
    links = Column(String, nullable=True)
    event = Column(String, nullable=True)
    distance = Column(String, nullable=True)
    places = Column(String, nullable=True)
    race_type = Column(String, nullable=True)

    def __init__(self, date, decline, links, event, distance, places, race_type):
        self.date = date
        self.decline = decline
        self.links = links
        self.event = event
        self.distance = distance
        self.places = places
        self.race_type = race_type

    def __repr__(self):
        return '<Occasion (event="{}", links="{}", date="{}", distance="{}", decline="{}", places="{}", race_type="{}")>'.format(
            self.event, self.links, self.date, self.distance, self.declien, self.places, self.race_type)
        
base.metadata.create_all(engine)

session = sessionmaker(bind=engine)()
