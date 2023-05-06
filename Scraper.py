print("starting...")

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()
import operator #for sorting, not used 
import datetime
import time
import mysql.connector
import urllib.request
import os
#import wget
#from PIL import Image
#from io import BytesIO

conn = mysql.connector.connect(
    host="localhost",
    user="evgeny",
    password="253321",
    database="AVITO_DB"
)
cursor = conn.cursor()

CAR_DB = {}
car = ['0-id', '1-date', '2-city', '3-make', '4-model', '5-year', '6-mileage', '7-power', '8-price', '9-link', '10-type', '11-wd', '12-fuel', '13-comment']
#car_list = ['acura', 'alfa_romeo', 'aston_martin', 'audi', 'baic', 'baw', 'bentley', 'bmw', 'brilliance', 'buick', 'byd', 'cadillac', 'changan', 'chery', 'chevrolet', 'chrysler', 'citroen', 'dacia', 'daewoo', 'daihatsu', 'daimler', 'datsun', 'derways', 'dodge', 'dongfeng', 'dw_hower', 'faw', 'ferrari', 'fiat', 'ford', 'gac', 'geely', 'genesis', 'gmc', 'great_wall', 'haima', 'haval', 'honda', 'hummer', 'hyundai', 'infiniti', 'iran_khodro', 'isuzu', 'iveco', 'jac', 'jaguar', 'jeep', 'jetta', 'jmc', 'kaiyi', 'kia', 'lamborghini', 'land_rover', 'lexus', 'lifan', 'lincoln', 'lixiang', 'lotus', 'maserati', 'mazda', 'mercedes-benz', 'mini', 'mitsubishi', 'morgan', 'neta', 'nio', 'nissan', 'opel', 'peugeot', 'polestar', 'porsche', 'ram', 'ravon', 'renault', 'renault_samsung', 'rivian', 'rolls_royce', 'rover', 'saab', 'saic', 'seat', 'seres', 'skoda', 'smart', 'ssangyong', 'subaru', 'suzuki', 'tank', 'tesla', 'tianye', 'toyota', 'volkswagen', 'volvo', 'vortex', 'zotye', 'vaz_lada', 'vis', 'gaz', 'zaz', 'izh', 'luaz', 'moskvich', 'tagaz', 'uaz']
car_list = ['audi', 'bentley', 'bmw', 'chery', 'chevrolet',  'ferrari', 'ford', 'geely', 'haval', 'honda', 'hummer', 'hyundai', 'kia', 'lamborghini', 'land_rover', 'lexus', 'mazda', 'mercedes-benz', 'mitsubishi', 'nissan', 'opel', 'peugeot', 'porsche', 'renault', 'rolls_royce', 'skoda', 'subaru', 'suzuki', 'tesla', 'toyota', 'volkswagen', 'vaz_lada', 'moskvich']
#car_list = ['ferrari']
def parse_avito(url, city_we_need):
        # Send a GET request to the URL
    response = requests.get(url, ua.random)
    print(response)

    # Parse the HTML content using BeautifulSoup 
    soup = BeautifulSoup(response.content, 'html.parser')

    #searching for the block of car ad
    items = soup.find_all('div', {'class': 'iva-item-root-_lk9K'})

    #parsing this block searching for the items:
    for item in items:
        try:
            #trying to search items in html here, sometimes there are mistakes
            #id
            car[0] = int(item.attrs.get('data-item-id'))

            #date
            car[1] = str(datetime.datetime.now().strftime("%Y-%m-%d"))# %H:%M:%S"))

            #city
            item_as_str = str(item)
            item_soup = BeautifulSoup(item_as_str, 'html.parser')
            #print(city_soup)
            address = item_soup.find('a', {'class': 'link-link-MbQDP'})#.text.strip()
            address = address.attrs.get('href')
            address = str(address)
            link = address
            #print(link)
            car[9] = str(link)
            address = address.split('/')
            address = address[1]
            category = address[2]
            car[2] = str(address)
                            
            #finding title (make model, year)
            item_as_str = str(item)
            #title_soup = BeautifulSoup(item_as_str, 'html.parser')
            title = item_soup.find('h3', {'class': 'title-root-zZCwT'}).text.strip()
            title = title.split(',') 
            make_and_model = title[0]
            make_and_model = make_and_model.split(' ')

            #make from title
            make = make_and_model[0]
            if make == 'ВАЗ':
                make = 'LADA'
            car[3] = str(make)

            #model from title
            del make_and_model[0] #deleting make
            if make_and_model[0] == '(LADA)':
                #deleting (LADA)
                del make_and_model[0]
            model = " ".join(make_and_model) #joining all the model words 'Grand Vitara'
            car[4] = str(model)

            #year from title
            year = title[1]
            car[5] = int(year)


            #milage
            #item_text_soup = BeautifulSoup(item_as_str, 'html.parser')
            item_text = item_soup.find('div', {'class': 'iva-item-text-Ge6dR text-text-LurtD text-size-s-BxGpL'}).text.strip()
           
            item_text = item_text.split(',')
            if item_text[0] == 'Битый':
                print('Битый')
                continue

            #if only 4 arguments are given then the car is new
            if len(item_text) == 4:
                #addin mileage to the list
                item_text.insert(0, 0)
                mileage = 0
                #print('new car..', item_text)
            else:
                mileage = item_text[0]
                mileage = mileage.replace(' ', '').rstrip('км')

            car[6] = int(mileage)

            #power
            power = item_text[1]
            power = power.split('(')
            power = power[1].split(' ')
            power = power[0]
            car[7] = int(power)

            #type
            type = item_text[2]
            type = type.split(' ')
            car[10] = str(type[1])

            #wd
            wd = item_text[3]
            wd = wd.split(' ')
            car[11] = str(wd[1])

            #fuel
            fuel = item_text[4]
            fuel = fuel.split(' ')
            car[12] = str(fuel[1])


            #finding price and converting to int (getting rid of words)
            #price_soup = BeautifulSoup(item_as_str, 'html.parser')
            price = item_soup.find('span', {'class': 'price-text-_YGDY'}).text.strip()
            price = price.replace(' ', '').rstrip('₽')
            price = price.split(' ')
            price = int(price[-1])
            car[8] = price

            #photo_soup = BeautifulSoup(item_as_str, 'html.parser')
            #photo = price_soup.find('img', {'class': 'photo-slider-image-YqMGj'})#.text.strip()

            photo = item_soup.find('li', {'class': 'photo-slider-list-item-h3A51'})#trying to find photo

            photo = photo.attrs.get('data-marker')
            photo = photo.split('slider-image/image-')
            #response_photo = requests.get(photo)
            #photo = Image.open(BytesIO(response_photo.content))
            photo = photo[1]
            try:
                comment = item_soup.find('div', {'class': 'iva-item-text-Ge6dR iva-item-description-FDgK4 text-text-LurtD text-size-s-BxGpL'}).text.strip()
                car[13] = str(comment)
            except:
                car[13] = 'no comments'

             
            #print(comment)



            #Saving to MySQL
            #filtering only needed city
            if car[2] == city_we_need:
                #checking if id is in db
                cursor.execute("SELECT id FROM cars WHERE id = %s", (car[0],))
                data=cursor.fetchone()
                if data is None:
                    #print('There is no id %s'%car[0])
                    cursor.execute('''INSERT INTO cars (id, date, city, make, model, year, mileage, power, price, link, type, wd, fuel, comment_text)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7], car[8], car[9], car[10], car[11], car[12], car[13]))
                    conn.commit()
                    print('new car found', car[2], car[3], car[4])

                    #saving on disk in a folder named as last digit of ID
                    folder = str(car[0])
                    folder = [int(d) for d in str(folder)]
                    folder = folder[-1]

                    #detects username and returns folder path
                    path = os.path.expanduser('~/img')
                    
                    urllib.request.urlretrieve(photo, f'{path}/{folder}/{car[0]}')
                else:
                    print('%s found in db'%(car[0]))                    
            else:
                print('city is not interested:', car[2])                
        except:
            print('something went wrong. skipping parsing this car...')



cities = ['moskva', 'ufa']#, 'sankt-peterburg', 'ufa'] #'vladivostok', 
#cities = ['ufa']

def generate_url():
    for city in cities:    
        for make in car_list:
                url = f'https://www.avito.ru/{city}/avtomobili/{make}?cd=1&radius=0&searchRadius=0'

                #GETTING MODELS
                response = requests.get(url, ua.random)
                print(response)

                # Parse the HTML content using BeautifulSoup 
                soup = BeautifulSoup(response.content, 'html.parser')

                #searching for the block of car ad
                links = soup.find_all('a', {'class': 'popular-rubricator-link-Hrkjd'})
                for link in links:
                    link = link.attrs.get('href')
                    print('link', link)
                    url = f'https://www.avito.ru{link}'
      
                    parse_avito(url, city)
                    time.sleep(10) #5 is ok

#start

generate_url() 
#parse_avito('https://www.avito.ru/moskva/avtomobili/bmw?cd=1', 'moskva')   
conn.close()


#end
#tried to get models from db- fail
#getting all available in db models of this make
#sql_query = "SELECT DISTINCT model FROM cars WHERE make = %s"
#cursor.execute(sql_query, (make,))
#resul}t = cursor.fetchall()
#sql_query = "SELECT link FROM `cars` WHERE model = %s LIMIT 1;"
#cursor.execute(sql_query, (model_car,))
#result_link = cursor.fetchall()
