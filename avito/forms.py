from django import forms
from django.forms import ModelForm
from avito.models import Cars

#HERE WE ARE BUILDING CHOICES LISTS GETTING IT FROM DATABASE AND CONVERTING TO NEEDED FORMAT (X, x) AND ADDING 'ALL'
def generate_make_choices():
    MAKE_CHOICES = []
    QUERY_MAKE_CHOICES = Cars.objects.order_by('make').values_list('make').distinct()
    for i in QUERY_MAKE_CHOICES:
        make = i[0]
        MAKE_CHOICES.append([make, make])
    MAKE_CHOICES.insert(0, (-1, "All"))
    return MAKE_CHOICES

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
        make = context[0].get('make')
        model = context[1].get('model')
        print("Forms.py CONTEXT:", make, model)
        if make == -1:
            model_choices = ((-1, "All"),)
        else:
            model_choices = generate_model_choices(make)
        
        super().__init__(*args, **kwargs)
        self.fields['make'] = forms.ChoiceField(choices = generate_make_choices(), initial = make)
        self.fields['model'] = forms.ChoiceField(choices=model_choices, initial = model)


