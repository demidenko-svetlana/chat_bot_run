import requests
from bs4 import BeautifulSoup, Tag

from database import Event, base, session

from parslets import calendar_page
from part1 import get_data, links

calendar_page()
get_data(links)