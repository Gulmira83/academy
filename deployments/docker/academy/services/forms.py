from django import forms
from .models import UserService
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

class UserServiceForm(forms.ModelForm):
    name = forms.CharField(label='Enter Name')
    class Meta:
        model = UserService
        fields = ('name', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserServiceFormDelete(DeleteView):
    model = UserService
    success_url = reverse_lazy('user-services')