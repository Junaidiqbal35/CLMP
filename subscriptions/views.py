import djstripe
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from accounts.models import User
from subscriptions.models import Membership, UserMembership, UserSubscription


def get_publishable_key(request):
    return JsonResponse({

        'publishableKey': 'pk_test_utELKNNX5QjQt9BTmkHlD71N00RZapjJeQ',
        'proPrice': 'price_1L2IKKI4e8u2GP8qehhvLKlj',

    })


@login_required
def create_checkout_session(request):
    try:
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1L2IKKI4e8u2GP8qehhvLKlj',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            customer_email=request.user.email,
            success_url='http://127.0.0.1:8000/subscription/' + 'success/{CHECKOUT_SESSION_ID}' + '/',
            cancel_url='http://127.0.0.1:8000/subscription/' + 'cancel' + '/',
        )
    except Exception as e:
        return HttpResponse(e)

    return redirect(checkout_session.url)


def get_checkout_session(request):
    id = request.args.get('sessionId')
    checkout_session = stripe.checkout.Session.retrieve(id)
    return HttpResponse(checkout_session)


# class CreateSubscriptionView(View, LoginRequiredMixin):
#     stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
#
#     def post(self, request, *args, **kwargs):
#         try:
#             price = request.data['price']
#             customer_id = request.data['customer_id']
#             customer_email = request.data['email']
#
#             # Create new Checkout Session for the order
#             # Other optional params include:
#             # [billing_address_collection] - to display billing address details on the page
#             # [customer] - if you have an existing Stripe Customer ID
#             # [customer_email] - lets you prefill the email input in the form
#             # For full details see https:#stripe.com/docs/api/checkout/sessions/create
#
#             # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#
#             checkout_session = stripe.checkout.Session.create(
#                 success_url='http://localhost:8000/success-sub/{CHECKOUT_SESSION_ID}',
#                 cancel_url='http://localhost:8000/cancel-sub',
#                 payment_method_types=['card'],
#                 customer=customer_id,
#                 allow_promotion_codes=True,
#                 mode='subscription',
#                 metadata={'price_id': price},
#                 line_items=[{
#                     'price': price,
#                     'quantity': 1
#                 }],
#
#             )
#             print(checkout_session)
#
#             return redirect(checkout_session.url)
#         except Exception as e:
#             print(e)
#             return render(request, 'subscriptions/plans.html')


# Fetch the Checkout Session to display the JSON result on the success page

class GetCheckoutSession(View):

    def get(self, request, session_id, *args, **kwargs):
        try:
            stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
            id = session_id
            checkout_session = stripe.checkout.Session.retrieve(id)
            customer = stripe.Customer.retrieve(id=checkout_session.customer)
            price_id = 'price_1L2IKKI4e8u2GP8qehhvLKlj'
            selected_membership = Membership.objects.get(stripe_plan_id=price_id)

            # fetch user data from UserMembership table
            user_membership = UserMembership.objects.get(user=request.user)

            user_membership.membership = selected_membership
            user_membership.subscription_badge = True
            user_membership.save()

            djstripe.models.Customer.sync_from_stripe_data(customer)

            subscription = stripe.Subscription.retrieve(id=checkout_session.subscription)
            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

            # for email purpose
            # data = {'username': user_membership.user.username, 'email': user_membership.user.email,
            #         'subscription_plan': subscription.plan.product}
            # send_email_after_subscription.delay(data)

            # subscription.subscription.plan.product -> fetch the plan name

            user_subscription = UserSubscription.objects.get(user_membership=user_membership)

            user_subscription.stripe_subscription_id = checkout_session.subscription
            user_subscription.subscription = djstripe_subscription

            user_subscription.save()
            user_membership_data = User.objects.get(email=request.user.email)
            user_membership_data.is_premium = True
            user_membership_data.save()

            return HttpResponse('success')
        except Exception as e:
            return HttpResponse(str(e))
