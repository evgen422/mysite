from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from django.db import models
from .models import Cars   #added avito and deleted
from django.http import HttpResponse
from django.template import loader
#from .forms import CarsForm #NameForm #CarsForm  #added avito and deleted
from .forms import CarsForm

def car_list(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        print('POST incoming...................', request.POST)

        make = request.POST.get("make")
        model = request.POST.get("model")
        print('make model', make, model)
        model = checking_model(make, model)
        print('make model', make, model)

        #CONSTRUCTING QUERY
        filter_params = {}
        if make != '-1':
            filter_params['make'] = make
            if model != '-1':
                 filter_params['model'] = model 
        print('filter_params', filter_params)       
        query = Cars.objects.filter(**filter_params)[:10] 
        filter_params = {}

        form = CarsForm(context=[{'make': make},{'model': model}])
        context = {
            'make': make,
            'model': model,
            'cars': query,
            'form': form,
        }
        return render(request, 'car_list.html', context)


    # if a GET (or any other method) we'll create a blank form
    else:
        query = Cars.objects.all()[:10]
        make = -1
        model = -1
        form = CarsForm(context=[{'make': make},{'model': model}])
        context = {
            'cars': query,
            'form': form,
        }
        return render(request, 'car_list.html', context)

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


        # create a form instance and populate it with data from the request:  NOT WORKING...
        #form = CarsForm(request.POST)
        # check whether it's valid:
        #if form.is_valid():