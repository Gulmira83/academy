from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Questions
from django.forms import ModelForm, Textarea


class faqForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = [ 'first_name', 'last_name', 'phone_number', 'email', 'subject', 'body']
        widgets = {
                    'body': Textarea(attrs={'cols': 40, 'rows': 20}),
                }



class UpdateInfo(forms.Form):
    first_name = forms.CharField(min_length=2, max_length=30)
    last_name = forms.CharField(min_length=2, max_length=30)
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(UpdateInfo, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        if not first_name or not last_name or not email:
            raise forms.ValidationError('Please enter required information')


class UpdateSettingsForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'username']



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = {
            'email',
            'username',
            'last_name',            
            'first_name',
            'password2',
            'password1',
        }
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']


        if commit:
            user.save()


        return user