
from django.urls import path
from . import views

urlpatterns = [
    path('student/register/', views.StudentAddView.as_view(), name='student-registration'),
    path('teacher/register/', views.TeacherAddView.as_view(), name='teacher-registration'),
]