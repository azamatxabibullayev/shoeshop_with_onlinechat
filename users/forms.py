from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Painting, Profile, Message


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PaintingForm(forms.ModelForm):
    class Meta:
        model = Painting
        fields = ['title', 'image']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']




















