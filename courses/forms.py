from crispy_forms.layout import Layout, Field
from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, Content, Comment


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


class CommentForm(forms.ModelForm):
    body = forms.TextInput()

    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = 'Leave a Comment'

        self.fields['body'].widget.attrs = {'rows': 2}
