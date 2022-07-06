
from django.urls import path
from . import views

urlpatterns = [
    path('student/register/', views.StudentAddView.as_view(), name='student-registration'),
    path('teacher/register/', views.TeacherAddView.as_view(), name='teacher-registration'),
    path('profile/<int:pk>/', views.UserProfile.as_view(), name='profile'),
    path('teacher/profile/update/<int:pk>/', views.TeacherProfileUpdateView.as_view(), name='teacher-update-profile'),
    path('student/profile/update/<int:pk>/', views.StudentProfileUpdateView.as_view(), name='student-update-profile'),
]