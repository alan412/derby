from django import forms
from django.forms import ModelForm, Form, ModelChoiceField
from derby.models import Car, Group


class CameraImageInput(forms.ClearableFileInput):
    template_name = 'django/forms/widgets/clearable_file_input.html'
    
    def __init__(self, attrs=None):
        default_attrs = {
            'accept': 'image/*',
            'capture': 'environment',  # Use rear camera on mobile devices
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class RegisterForm(ModelForm):
    class Meta:
        model = Car
        fields = ['owner', 'name', 'group', 'picture']
        labels = {
            'name': 'Car Name',
        }
        widgets = {
            'picture': CameraImageInput(),
        }
