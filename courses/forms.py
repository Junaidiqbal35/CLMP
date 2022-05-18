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
        fields = ['module', 'title', 'video']


ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title',
                                              'description'],
                                      extra=2,
                                      can_delete=True)
