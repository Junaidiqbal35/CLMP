from django.urls import path
from django.views.generic import TemplateView

from .views import create_checkout_session, get_publishable_key, GetCheckoutSession

urlpatterns = [
    path('config', get_publishable_key, name='config'),
    path('create-subscription/', create_checkout_session, name='create-subscription'),
    path('success/<str:session_id>/', GetCheckoutSession.as_view(), name='get-checkout-session'),
   # path('success/', TemplateView.as_view(template_name="subscriptions/success.html"), name='success'),
    path('cancel/', TemplateView.as_view(template_name="subscriptions/canceled.html"), name='canceled'),

]
