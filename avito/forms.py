from django import forms
from django.forms import ModelForm
from avito.models import Cars

#HERE WE ARE BUILDING CHOICES LIST GETTING IT FROM DATABASE AND CONVERTING TO NEEDED FORMAT (X, x)
MAKE_CHOISES = Cars.objects.order_by('make').values_list('make', 'make').distinct()


#                                     DEPRICATED
#MAKE_CHOISES = []
#for i in GET_MAKE_CHOISES:
#    make = i['make']
#    MAKE_CHOISES.append([make, make])

MODEL_CHOICES = (
    ('choose','choose'),
)


class CarsForm(forms.Form):# YOU EITHER MAKE FIELDS HERE WITH USUAL FORM OR go to model if ModelForm
    
    make = forms.ChoiceField(choices = MAKE_CHOISES)
    model = forms.ChoiceField(choices = MODEL_CHOICES)



class CarsForm_with_selected_make(forms.Form):# YOU EITHER MAKE FIELDS HERE WITH USUAL FORM OR go to model if ModelForm
    #extracting context
    def __init__(self, *args, **kwargs):
        context = kwargs.pop('context', {})
        print("CONTEXT?????????", context)
        selected_by_user_make = context[0].get('selected_by_user_make')
        selected_by_user_model = context[1].get('selected_by_user_model')
        print("CONTEXT?????????", selected_by_user_make, selected_by_user_model)
        choices = Cars.objects.filter(make=selected_by_user_make).order_by('model').values_list('model', 'model').distinct()
        print('forms make , choices: ', selected_by_user_make, choices)
        
#FINALLY IT WORKS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        super().__init__(*args, **kwargs)
        MADE_CHOICE = (
        (selected_by_user_make,selected_by_user_make),
        )
        self.fields['make'] = forms.ChoiceField(choices=MADE_CHOICE)
        self.fields['model'] = forms.ChoiceField(choices=choices, initial = selected_by_user_model)


#YOU EITHER CLEAR IT HERE OR IN THE VIEW: NOT BOTH
#    def clean(self):
#        test = self.cleaned_data['test']
#        #print(self)
#        print('cleaned in form...........', test)
#        valid_choices = dict(GEEKS_CHOICES).keys()
#
#        if test not in valid_choices:
 #           raise forms.ValidationError(f'{test} is not a valid choice.')
 #       else:
 #           print('test is valid', test)
#
 #           return test


