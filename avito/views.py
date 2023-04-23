from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from django.db import models
from .models import Cars   #added avito and deleted
from django.http import HttpResponse
from django.template import loader
from .forms import CarsForm #NameForm #CarsForm  #added avito and deleted



#def index(request):

def car_list(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        print('POST incoming...................')
        # create a form instance and populate it with data from the request:
        form = CarsForm(request.POST)
        print('form............', form)
        # check whether it's valid:
        if form.is_valid():
            wanted_by_user_make = form.cleaned_data["make"]
            print('make....................', wanted_by_user_make)

            cars = Cars.objects.filter(make = wanted_by_user_make)[:10] #make = request.your_name ??????????
            print(cars)
            form = CarsForm()
            context = {
                'cars': cars,
                'form': form,
            }
            return render(request, 'car_list.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        cars = Cars.objects.all()[:10]
        form = CarsForm() #NameForm()
        context = {
            'cars': cars,
            'form': form,
        }
        return render(request, 'car_list.html', context)