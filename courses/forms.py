from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, Content


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['created_at', 'slug']


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['module', 'title']


ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title',
                                              'description'],
                                      extra=6,
                                      can_delete=True)


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
