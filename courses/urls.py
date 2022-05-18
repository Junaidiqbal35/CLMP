from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('mine/',
         views.ManageCourseListView.as_view(),
         name='manage_course_list'),
    path('create/',
         views.CourseCreateView.as_view(),
         name='course_create'),
    path('<pk>/edit/',
         views.CourseUpdateView.as_view(),
         name='course_edit'),
    path('<pk>/delete/',
         views.CourseDeleteView.as_view(),
         name='course_delete'),
    path('<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    path('module/<int:module_id>/content/create/',
         views.ContentCreateUpdateView.as_view(),
         name='module_content_create'),

    path('', TemplateView.as_view(template_name="courses/courses.html"), name='courses'),
    path('detail/', TemplateView.as_view(template_name="courses/course_detail.html"))

]
