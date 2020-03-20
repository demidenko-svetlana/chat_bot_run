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
        #page_number = soup.find('ul', {"class": "pagination"}).findAll('li')
        #last_number = []
        for sibling in soup.find('li', {"class": "next"}).previous_sibling.previous_sibling:
            page = int(sibling.contents[0])

    print(page)
    #     for numbers in page_number:
    #         number = numbers.find('a')
    #         if number: 
    #             last_number.append(number.text)
    #             #return last_number[len(last_number)-2]
    # print(last_number[-2])


print(last_page())        
        


# def get_data():
#     html = get_html("https://get.run/races/europe/russia")
#     webname = 'https://get.run'
#     if html:
#         soup = BeautifulSoup(html, 'html.parser')
#         all_data = soup.findAll('div', class_="cont")
#         result_data = []
#         for data in all_data:
#             title = data.find('span').text
#             url = data.find('a')['href']
#             # calendar = data.find
#             result_data.append({
#                 "title": title,
#                 "url": webname + url 
#             })
#         return result_data
#     return False
# #page_data = get_data()           
# print(get_data())
