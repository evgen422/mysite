from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from django.db import models
from .models import Cars   #added avito and deleted
from django.http import HttpResponse
from django.template import loader
#from .forms import CarsForm #NameForm #CarsForm  #added avito and deleted
from .forms import CarsForm


#def index(request):

def car_list(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        print('POST incoming...................', request.POST)
        # create a form instance and populate it with data from the request:
        #form = CarsForm_with_selected_make(context={'selected_by_user_make': selected_by_user_make})
        #print('form............', form)
        # check whether it's valid:
        #if form.is_valid():

        make = request.POST.get("make")
        model = request.POST.get("model")
        print('form cleaned............', make, model)

        cars = Cars.objects.filter(make = make, model = model)[:10] #make = request.your_name ??????????
        #print('views.py: cars....................', cars)
        form = CarsForm(context=[{'make': make},{'model': model}])
        context = {
            'make': make,
            'model': model,
            'cars': cars,
            'form': form,
        }
        return render(request, 'car_list.html', context)


    # if a GET (or any other method) we'll create a blank form
    else:
        cars = Cars.objects.all()[:10]
        #form = CarsForm() #NameForm()
        make = -1
        model = -1
        form = CarsForm(context=[{'make': make},{'model': model}])
        context = {
            'cars': cars,
            'form': form,
        }
        return render(request, 'car_list.html', context)