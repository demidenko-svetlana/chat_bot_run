import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):  # проверяет работает ли сайт
        print("Web error")
        return False


def last_page():
    html = get_html("https://get.run/races/europe/russia")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for sibling in soup.find('li', {"class": "next"}).previous_sibling.previous_sibling:  # ищет количество страниц на сайте
            page = int(sibling.contents[0])
            url_new = "https://get.run/races/europe/russia/?PAGEN_3={}"
            links = []                # формирует список страниц сайта 
            for page_number in range(1, page + 1):
                links.append(url_new.format(page_number))
    return links 


links = last_page()


def get_distance(tags):  # функция поиска и формирования списка дистанций
        d = []
        for distance in tags:
            d.append(distance.contents[0])
        distances = ' , '.join(d)
     
        return distances


def get_data(links):
    result_data = []
    for link in links:   # проходит по всем страницам
        html = get_html(link)
        webname = 'https://get.run'
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            info = soup.find('div', {"id": "confirmed"}) # из списка с соответствующими тегами,ищет следующие теги для каждой переменной
            all_data = info.find_all('div', {"class": "text"})
            for data in all_data:
                title = data.find('div',{"class": "title"})
                url = data.find('a')
                place = data.find_all('div', {"class": "article"})
                kindof = data.findAll('div', {"class": "article"})
                race_date = data.find('div', {"class": "price"})
                distance_tags = data.find_all('span', {"class":"label"})
                distances = get_distance(distance_tags)
                if (title and url and place and kindof and race_date):  # проверяет на пустые значения и записывает только те, что не None
                    name = title.find('span').text
                    n_url = url.get('href')
                    location = place[0].text
                    kind = kindof[1].text
                    date = race_date.find('span').text
                result_data.append({         # список необходимых атрибутов
                    "event": name,
                    "links": webname + n_url,
                    "places": location,
                    "race_type": kind,
                    "date": date,
                    "distance": distances,
                    "decline": "Подробности о статусе забега вы можете узнать, перейдя по ссылке"
                    "country": "Россия"
                })

    print(result_data)

    return result_data


get_data(links)