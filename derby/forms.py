from django.forms import ModelForm
from derby.models import Car


class RegisterForm(ModelForm):
    class Meta:
        model = Car
        fields = ['owner', 'name', 'group', 'picture']
        labels = {
            'name': 'Car Name',
        }
