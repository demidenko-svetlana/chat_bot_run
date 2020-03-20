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
            url_new = "https://get.run/races/europe/russia/?PAGEN_3 ={}"
            links = []                
            for page_number in range(1, page + 1):
                links.append(url_new.format(page_number))
    return links     
links = last_page()

#print(last_page())        
        

def get_data(links):
    for link in links:
        html = get_html(link)
        webname = 'https://get.run'
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            all_data = soup.findAll('div', class_="text")
            result_data = []
            for data in all_data:#soup.findAll('div', class_="text"):
                #data = soup.find('div', class_="cont")
                title = data.find('div', {"class" : "title"}).find('a').text
                url = data.find('a')['href']
                # calendar = data.find
                result_data.append({
                    "title": title,
                    "url": webname + url 
                })
            return result_data
        print(result_data)
            #return False
    #page_data = get_data()           
print(get_data(links))
