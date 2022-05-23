from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('plans/', TemplateView.as_view(template_name="subscriptions/plans.html"), name='plans'),
                  path('', include('courses.urls')),

                  path('accounts/', include('accounts.urls')),
                  path('accounts/', include('allauth.urls')),
                  path('subscription/', include('subscriptions.urls')),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
