# Django + MySQL. Avito.ru simulator

## Introduction

This project shows the apllication of Django and MySQL in eCommerce industry. First we use [Scraper.py](https://github.com/evgen422/mysite/blob/main/Scraper.py) to parse Avito and collect used car database. Then we use Django to serve the database to user. 
Deployed app can be found at http://45.95.235.237/avito/

## Description

The code that is responsible for scraping and parsing Avito.ru is located at [Scraper.py](https://github.com/evgen422/mysite/blob/main/Scraper.py).

1) We start by generating url that we want to parse. It consists of a city and a car make. 
```
url = f'https://www.avito.ru/{city}/avtomobili/{make}?cd=1&radius=0&searchRadius=0
```
2) We use Fake_User_Agent to generate random user agents so the server won't block us immidiatly.

3) After the response with links to all the models for this make is recieved, we loop over the links and send them to parsing function.
```
for link in links:
    link = link.attrs.get('href')
    url = f'https://www.avito.ru{link}'
    parse_avito(url, city)
```
4) After parsing code is put to sleep for several seconds to prevent blocking from the server.

5) As parsing function is called, it requests a page for the model we need.
```
response = requests.get(url, ua.random)
```
6) Parsing the HTML content using BeautifulSoup
```
soup = BeautifulSoup(response.content, 'html.parser')
```
7) Searching for the block of a car ad. This block contains all the information about the car
```
items = soup.find_all('div', {'class': 'iva-item-root-_lk9K'})
```
8) Parsing this block searching for the car properties such as ID, mileage, price and so on:
```
for item in items:
    car[0] = int(item.attrs.get('data-item-id'))
```
9) Saving to MySQL if car is not in db yet:
```
cursor.execute('''INSERT INTO cars (id, date, city, make, model, year, mileage, power, price, link, type, wd, fuel, comment_text)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], car[10], car[11], car[12], car[13]))
conn.commit()
```
10) Saving image of the car on disk in a folder named as last digit of ID
```
photo = item_soup.find('li', {'class': 'photo-slider-list-item-h3A51'})
urllib.request.urlretrieve(photo, f'{path}/{folder}/{car[0]}')
```