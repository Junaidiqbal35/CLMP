from django import forms
from django.contrib.auth.password_validation import validate_password
from django.forms import PasswordInput

from accounts.models import User, Student, Teacher


class CreateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    password = forms.CharField(widget=PasswordInput(), validators=[validate_password])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['city', 'qualification']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['city', 'qualification']