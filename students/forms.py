from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from courses.models import Course
from .models import Profile


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class StudentUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)