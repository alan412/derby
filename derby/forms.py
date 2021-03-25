from django import forms
from derby.models import Group


class RegisterForm(forms.Form):
    owner = forms.CharField(label='Owner Name', max_length=64)
    carName = forms.CharField(label="Car Name", max_length=64)
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    img = forms.ImageField(label="Car Photo")
