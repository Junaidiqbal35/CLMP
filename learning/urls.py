from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [

                  path('course/', include('courses.urls')),
                  path('plans/', TemplateView.as_view(template_name="subscriptions/plans.html"), name='plans'),
                  path('accounts/', include('accounts.urls')),
                  path('accounts/', include('allauth.urls')),

                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
