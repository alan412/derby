from django.forms import ModelForm, Form, ModelChoiceField
from derby.models import Car, Group


class RegisterForm(ModelForm):
    class Meta:
        model = Car
        fields = ['owner', 'name', 'group', 'picture']
        labels = {
            'name': 'Car Name',
        }

class SelectGroupForm(Form):
    group = ModelChoiceField(queryset=Group.objects.all())