# Django + MySQL. Avito.ru simulator

## Introduction

This project shows the apllication of Django and MySQL in eCommerce industry. First we use [Scraper.py](https://github.com/evgen422/mysite/blob/main/avito/Scraper.py) to parse Avito and collect used car database. Then we use Django to serve the database to user. <br>
Deployed app can be found at http://45.95.235.237/avito/<br>
[Database](https://drive.google.com/file/d/1TmwYdSoXiqJpTFmlksCUHLH4IS08XJhi/view?usp=sharing) with 20000 parsed cars from avito<br>
[Archive](https://drive.google.com/file/d/1GceJOu9f3VKMqY0CR749n2RwreVC4RZ9/view?usp=sharing) with photos of 20000 cars

## Populating the database

The code that is responsible for scraping and parsing Avito.ru is located at [Scraper.py](https://github.com/evgen422/mysite/blob/main/avito/Scraper.py).

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
4) After parsing is done we put code to sleep for several seconds to prevent blocking from the server.

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
8) Parsing this block and searching for the car properties such as ID, mileage, price and so on:
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

## Django app

1) When a user opens web-page first time, [urls.py](https://github.com/evgen422/mysite/blob/main/avito/urls.py) serves it a function car_list(request) from [views.py](https://github.com/evgen422/mysite/blob/main/avito/views.py)
```
urlpatterns = [
    path('', views.car_list, name='car_list'),
```
2) First time the method of request is GET, so we call function send_initial_values(request) and send a form with default search parameters.
```
if request.method == "POST":
else:
    context = send_initial_values(request)
    return render(request, 'car_list.html', context)
```
3) We import form 'CarsForm' from [forms.py](https://github.com/evgen422/mysite/blob/main/avito/forms.py)
```
from .forms import CarsForm
```
4) And populates search fields with default values
```
class CarsForm(forms.Form):
    city = context['city']
    self.fields['city'] = forms.ChoiceField(choices = generate_make_choices('city'), initial = city)
```
5) Function "generate_make_choices" sends value (i.e. 'city') to the database and retrieves all available cities (i.e. Moskva, Ufa)
```
def generate_make_choices(value):
    QUERY = Cars.objects.order_by(value).values_list(value).distinct()
```
6) The form imports model 'Cars' from [models.py](https://github.com/evgen422/mysite/blob/main/avito/models.py)
```
from avito.models import Cars
```
7) The model contains information about the car from MySQL, table 'cars'
```
class Cars(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    make = models.TextField(blank=True, null=True, choices=MAKE_CHOICES, default='audi')
...
    class Meta:
        managed = False
        db_table = 'cars'
```
8) When views.py function collects form, it sends it to user together with a template [car_list.html](https://github.com/evgen422/mysite/blob/main/avito/templates/car_list.html)
```
return render(request, 'car_list.html', context)
```
9) The template extends base template [base.html](https://github.com/evgen422/mysite/blob/main/templates/base.html)
```
{% extends 'base.html' %}
```
10) which containes Bootstrap Navbar
```
<nav class="navbar navbar-expand-lg navbar-light bg-primary">
```
11) Then the template is devided into columns with Bootstrap: left column is Search form. It containes search fields:
```
<form method="post" id="search-form" name="search-form">
{% csrf_token %}
<div class="form-group">
  <label for="{{ form.city.id_for_label }}">City:</label>
  {% render_field form.city|add_class:"form-control custom-select" %}  
```

12) Right column is for Results 
```
<div class="col-md-8 col-sm-12 mb-3 px-0 result_col">
  <h4 class="h4 px-3">Search Results</h4>
    <!-- Loop through results and create cards for each -->
    {% for car in cars %}
```
13) jQuery script listens for the 'change' event in the search fields. When a user changes value (i.e changing default city Moskva to Ufa), Ajax script sends request to the server to update page automatically so user doesnt need to press any 'send' buttons.
```
$(document).ready(function() {
$('#id_city, #id_make, #id_model, #id_year_min, #id_year_max, #id_mileage_min, #id_mileage_max, #id_power_min, #id_power_max, #id_price_min, #id_price_max, #id_type, #id_wd, #id_fuel').change(function() {
    $.ajax({
        type: "POST",
        url: "{% url 'car_list' %}",
        data: $('#search-form').serialize(),
        success: function(response) {
            $('body').html(response);
```
14) When forms.py receives POST request, it parses values:
```
city = request.POST.get("city")
```
15) Then it constructs QUERY to database
```
filter_params['year__range']=(year_min, year_max)
```
16) and filters objects in database
```
query = Cars.objects.filter(**filter_params)[:20] 
```
17) then it sends results back to user:
```
context = {
    'cars': query,
    'form': form,
}
return render(request, 'car_list.html', context) 
```
18) img_view serves images from a folder on disk to the webpage:
```
img_view(request, car_id):
    if car.id:
        for i in str(car_id):
            last_digit = i
        image_path = os.path.join('/home/evgeny/img/',last_digit, str(car_id)) 
        f = open(image_path, 'rb')
        response = FileResponse(f, content_type='image/webp')
        response['Content-Disposition'] = 'inline; filename=%s' % car.id
        return response
```
19) single_car_view is called when a user clicks on a certain car card. It opens a new page with detailed information about the car.
```
single_car_view(request, car_id):
    car = get_object_or_404(Cars, pk=car_id)
    context = {'car': car}
    return render(request, 'single_car.html', context)
```
