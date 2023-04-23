from django import forms
from django.forms import ModelForm
from avito.models import Cars

GET_MAKE_CHOISES = Cars.objects.order_by().values('make').distinct()
MAKE_CHOISES = []
for i in GET_MAKE_CHOISES:
    make = i['make']
    MAKE_CHOISES.append([make, make])

print(MAKE_CHOISES)

class CarsForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ('make',)#, 'model', 'year')
    
    make = forms.ModelChoiceField(queryset=Cars.objects.order_by().values('make').distinct())#, choices = MAKE_CHOISES)#, default = 'audi')
    #model = forms.CharField(label="model", blank=True)
    #year = forms.IntegerField(label="year", blank=True)



class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)