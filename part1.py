import requests
from bs4 import BeautifulSoup


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Web error")
        return False


def last_page():
    html = get_html("https://get.run/races/europe/russia")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        for sibling in soup.find('li', {"class": "next"}).previous_sibling.previous_sibling:
            page = int(sibling.contents[0])
            url_new = "https://get.run/races/europe/russia/?PAGEN_3={}"
            links = []                
            for page_number in range(1, page + 1):
                links.append(url_new.format(page_number))
    return links     
links = last_page()

#print(last_page()) 


# def get_distance(tag):
#     for link in links:
#         html = get_html(link)    
#         soup = BeautifulSoup(html, 'html.parser')
#         dist = soup.findAll('span', class_ = "label")
#         d = []
#         for distance in dist:
#             d.append(distance.contents[0])
#         distances = ' , '.join(d)

#     #print(distances)        


def get_data(links):
    result_data = []
    for link in links:
        html = get_html(link)
        webname = 'https://get.run'
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            info = soup.find('div', id = "confirmed")
            all_data = info.findAll('div', {"class":"text"})
            for data in all_data:
                title = data.find('div',class_ = "title")
                url = data.find('a')
                place = data.findAll('div',class_ =  "article")
                kindof = data.findAll('div',class_ = "article")
                race_date = data.find('div', class_ = "price")
                #distances = get_distance(data)
                if (title and url and place and kindof and race_date):
                    name = title.find('span').text
                    n_url = url.get('href')
                    location = place[0].text
                    kind = kindof[1].text
                    date = race_date.find('span').text
                    #distance = distances.find('span')
               
                result_data.append({
                    "title": name,
                    "url": webname + n_url,
                    "location": location, 
                    "kind" : kind,
                    "date" : date  
                    #"distance" : distances
                })

    print(result_data)

    return result_data
   

get_data(links)