from django.shortcuts import render

# Create your views here.
from django.db import models
from .models import Cars
from django.http import HttpResponse
from django.template import loader
from .forms import CarsForm



def index(request):
    if request.method == 'POST':
        # Retrieve the product ID submitted by the user in the HTML form
        car_make = request.POST.get('car_make', '')
        
        # Fetch the product from the database
        car = Cars.objects.get(make=car_make)
    
    # Get all products from the database
    cars = Cars.objects.all()
    
    # Pass the fetched products to the HTML template
    template = loader.get_template("avito/index.html")
    context = {'cars': cars}
    return HttpResponse(template.render(context, request))
    #return render(request, 'index.html', context)

def car_make_list(request):
    form = CarForm()

    context = {
        'form': form,
    }

    return render(request, 'car_make_list.html', context)

def top_makes(request):
    top_makes = Cars.objects.values('make').annotate(count=models.Count('make')).order_by('-count')[:10]
    # top_makes will be a queryset with the top 10 makes and their counts

    context = {
        'top_makes': top_makes,
    }

    return render(request, 'top_makes.html', context)

