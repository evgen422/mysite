from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from django.db import models
from .models import Cars   #added avito and deleted
from django.http import HttpResponse
from django.template import loader
#from .forms import CarsForm #NameForm #CarsForm  #added avito and deleted
from .forms import CarsForm
from django.http import FileResponse
import os
from PIL import Image
from django.shortcuts import get_object_or_404

def car_list(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        print('POST incoming...................', request.POST)

        if request.POST.get("refresh") == '1':
            print('REFRESH incoming...................')
            context = send_initial_values(request)
            return render(request, 'car_list.html', context)              

        city = request.POST.get("city")
        make = request.POST.get("make")
        model = request.POST.get("model")

        year_min = request.POST.get("year_min")
        year_max = request.POST.get("year_max")

        mileage_min = request.POST.get("mileage_min")
        mileage_max = request.POST.get("mileage_max")

        power_min = request.POST.get("power_min")
        power_max = request.POST.get("power_max")

        price_min = request.POST.get("price_min")
        price_max = request.POST.get("price_max")

        type = request.POST.get("type")
        wd = request.POST.get("wd")
        fuel = request.POST.get("fuel")

        #checking because make has changed but model not, so its like BMW 100 or Audi M3
        model = checking_model(make, model)

        #CONSTRUCTING QUERY (-1 means parameter won't get into the filter)
        filter_params = {}
        if make != '-1':
            filter_params['make'] = make
            if model != '-1':
                 filter_params['model'] = model 
        parameters ={'city': city, 'type': type, 'wd': wd, 'fuel': fuel}
        for key, value in parameters.items():#for param in parameters:
            print(key, value)
            if value != '-1':
                filter_params[key] = value

        filter_params['year__range']=(year_min, year_max)
        filter_params['mileage__range']=(mileage_min, mileage_max)
        filter_params['power__range']=(power_min, power_max)
        filter_params['price__range']=(price_min, price_max)

        print('filter_params', filter_params)       
        query = Cars.objects.filter(**filter_params)[:20] 
        filter_params = {}

        form = CarsForm(context={
            'city': city,
            'make': make,
            'model': model,            
            'year_min': year_min,
            'year_max': year_max,
            'mileage_min': mileage_min,
            'mileage_max': mileage_max,
            'power_min': power_min,
            'power_max': power_max,
            'price_min': price_min,
            'price_max': price_max,
            'type': type,
            'wd': wd,
            'fuel': fuel,
            })
        context = {
            #'city': city,
            #'make': make,
            #'model': model,            
            'cars': query,
            'form': form,
        }
        return render(request, 'car_list.html', context)


    # if a GET (or any other method) we'll create a blank form
    else:
        print('GET incoming...................')
        context = send_initial_values(request)
        return render(request, 'car_list.html', context)
        
def send_initial_values(request):
    query = Cars.objects.all()[:10]

    city = -1
    make = -1
    model = -1
    year_min = 1990
    year_max = 2023
    mileage_min = 0
    mileage_max = 300000
    power_min = 0
    power_max = 1200
    price_min = 0
    price_max = 40000000
    type = -1
    wd = -1
    fuel = -1

    form = CarsForm(context={
        'city': city,
        'make': make,
        'model': model,            
        'year_min': year_min,
        'year_max': year_max,
        'mileage_min': mileage_min,
        'mileage_max': mileage_max,
        'power_min': power_min,
        'power_max': power_max,
        'price_min': price_min,
        'price_max': price_max,
        'type': type,
        'wd': wd,
        'fuel': fuel,
        })
    context = {
        'cars': query,
        'form': form,
    }
    return context
        

def checking_model(make, model):
    if make == '-1':
        model = '-1'
        return model
    if model == '-1':
        return model

    model_list = []
    query = Cars.objects.filter(make=make).order_by('model').values_list('model').distinct()
    for i in query:
        x = i[0]
        model_list.append(x)
    if model in model_list:
        return model
    else:
        model = '-1'
        print('changed wrong model to -1')
        return model

def img_view(request, car_id):
    #print(request, car_id)
    car = get_object_or_404(Cars, pk=car_id)
    if car.id:
        for i in str(car_id):
            last_digit = i
        image_path = os.path.join('/home/evgeny/img/',last_digit, str(car_id)) 
        f = open(image_path, 'rb')
        response = FileResponse(f, content_type='image/webp')
        response['Content-Disposition'] = 'inline; filename=%s' % car.id
        return response

def single_car_view(request, car_id):
    car = get_object_or_404(Cars, pk=car_id)
    print('404', car)
    if car.id:
        for i in str(car_id):
            last_digit = i
        image_path = os.path.join('/home/evgeny/img/',last_digit, str(car_id)) 
        context = {'car': car}
        return render(request, 'single_car.html', context)