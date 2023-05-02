from django import forms
from django.forms import ModelForm
from avito.models import Cars
from django_range_slider.fields import RangeSliderField

#HERE WE ARE BUILDING CHOICES LISTS GETTING IT FROM DATABASE AND CONVERTING TO NEEDED FORMAT (X, x) AND ADDING 'ALL'

def generate_make_choices(value):
    CHOICES = []
    QUERY = Cars.objects.order_by(value).values_list(value).distinct()
    for i in QUERY:
        x = i[0]
        CHOICES.append([x, x])
    CHOICES.insert(0, (-1, "All"))
    return CHOICES

def generate_model_choices(make):
    MODEL_CHOICES = []
    QUERY_MODEL_CHOICES = Cars.objects.filter(make=make).order_by('model').values_list('model').distinct()
    for i in QUERY_MODEL_CHOICES:
        model = i[0]
        MODEL_CHOICES.append([model, model])
    MODEL_CHOICES.insert(0, (-1, "All"))
    return MODEL_CHOICES

class CarsForm(forms.Form):# YOU EITHER MAKE FIELDS HERE WITH USUAL FORM OR go to model if ModelForm
    #extracting context
    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        print(context)
        city = context['city']
        make = context['make']
        model = context['model']
        year_min = context['year_min']
        year_max = context['year_max']
        mileage_min = context['mileage_min']
        mileage_max = context['mileage_max']
        power_min = context['power_min']
        power_max = context['power_max']
        price_min = context['price_min']
        price_max = context['price_max']
        type = context['type']
        wd = context['wd']
        fuel = context['fuel']
        print("Forms.py CONTEXT:", context)

        #if make == -1:
        #    model_choices = ((-1, "All"),)
        #else:
        model_choices = generate_model_choices(make)
        
        super().__init__(*args, **kwargs)
        self.fields['city'] = forms.ChoiceField(choices = generate_make_choices('city'), initial = city)
        self.fields['model'] = forms.ChoiceField(choices=generate_model_choices(make), initial = model)
        self.fields['make'] = forms.ChoiceField(choices = generate_make_choices('make'), initial = make)

        self.fields['year_min'] = forms.IntegerField(initial = year_min)
        self.fields['year_max'] = forms.IntegerField(initial = year_max)
        
        self.fields['mileage_min'] = forms.IntegerField(initial = mileage_min)
        self.fields['mileage_max'] = forms.IntegerField(initial = mileage_max)

        self.fields['power_min'] = forms.IntegerField(initial = power_min)
        self.fields['power_max'] = forms.IntegerField(initial = power_max)        

        self.fields['price_min'] = forms.IntegerField(initial = price_min)
        self.fields['price_max'] = forms.IntegerField(initial = price_max)        
        self.fields['type'] = forms.ChoiceField(choices = generate_make_choices('type'), initial = type)
        self.fields['wd'] = forms.ChoiceField(choices = generate_make_choices('wd'), initial = wd)
        self.fields['fuel'] = forms.ChoiceField(choices = generate_make_choices('fuel'), initial = fuel)


# forms.py
#class SliderForm(forms.Form):
#     name_range_field = RangeSliderField(minimum=30,maximum=300,name="TestName") # with name inside the input field (no label)
#     range_field = RangeSliderField(minimum=10,maximum=102) # without name or label
#     label_range_field = RangeSliderField(label="TestLabel",minimum=1,maximum=10) # with label (no name)