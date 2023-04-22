from django import forms
from .models import Cars

class CarsForm(forms.Form):
    car_make = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['make'].choices = [(make, make) for make in Cars.objects.values_list('make', flat=True).distinct()]