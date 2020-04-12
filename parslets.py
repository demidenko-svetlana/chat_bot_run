import requests
from bs4 import BeautifulSoup, Tag

from database import Event, base, session

def get_html(url):
    try:
        result = requests.get(url, timeout=5)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False


def calendar_page():
    response = get_html('https://letsportpeople.com/ru/year-2020-races_ru/')

    soup = BeautifulSoup(response, 'html.parser')
    calendar = soup.find_all('div')
    
    month_tag = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    monthes = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}

    month = None                               
    for t in calendar:
        d = {}   # словарь, куда записываем все нужные данные со страницы и на основании которого строится БД
        h2_month = t.find('h2')
        if h2_month:
            month_tag = h2_month.find('a')
            month = month_tag.get('id')
            if month in monthes:
                month = monthes[month]
                
        tag_s = t.find('h5')
        if tag_s:
            tag_day = tag_s.text
            
            decline = t.find('s')
            if decline:
                d['decline'] = 'Отменено'
            else:
                d['decline'] = 'Без изменений'
            href = t.find('a')
            if href:
                links = href.get('href')
                if links:
                    d['links'] = links
                    d['race_type'] = 'Шоссейный'
                
                country = type(t.find('br').next_sibling)
                if country is Tag:
                    d['country'] = t.find('br').next_sibling.next_sibling.next_sibling
                else:
                    d['country'] = t.find('br').next_sibling

                event_text = href.text
                if event_text:
                    if 'Календарь забегов' in event_text:
                        continue
                    else:
                        d['event_name'] = event_text
                        d['date'] = f'{tag_day}.{month}.2020'
                        if d['country'].strip() == 'Россия':
                            d['location'] = 'Россия'
                        else:
                            d['location'] = 'За рубежом'
                    dist = t.find_all('strong')
                    if dist:
                        dist = dist[-1].text.replace('M', '42.195 км').replace('U', '45.595 км').replace('H', '21.097 км').replace('М', '42.195 км').replace('Н', '21.097 км')
                        d['distance'] = dist 
                        save_event(d)

def save_event(d):
    event_data = Event(date=d['date'], decline=d['decline'], links=d['links'], event=d['event_name'], distance=d['distance'], places=d['country'], 
                    race_type=d['race_type'], country=d['location'])
    session.add(event_data)
    session.commit()