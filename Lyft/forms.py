from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ride

class CustomLoginForm(AuthenticationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
    )

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class MyUserCreationForm(UserCreationForm):
    username = forms.RegexField(label=("Email"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = ("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': ("This value may contain only letters, numbers and @/./+/-/_ characters.")})


class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = [ 'passenger_location', 'destination', 'available_seats']
        
