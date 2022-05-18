from django.urls import path
from .views import UserSubscriptionDetail, CreateSubscriptionApiView, GetCheckoutSession,\
    GetCheckoutSessionData, CreateCustomerPortalApiView, webhook_received
urlpatterns = [
    path('user-subscription/detail/', UserSubscriptionDetail.as_view(), name='subscription-detail'),
    path('create-subscription/', CreateSubscriptionApiView.as_view(), name='create-subscription'),
    path('get-checkout-session/<str:session_id>/', GetCheckoutSession.as_view(), name='get-checkout-session'),
    path('get-checkout-session-data/<str:username>/', GetCheckoutSessionData.as_view(), name='get-checkout-session-data'),
    path('create-customer-portal/', CreateCustomerPortalApiView.as_view(), name='create-customer-portal'),
    path('stripe/webhook/received/', webhook_received, name='webhook-received-view')


]
