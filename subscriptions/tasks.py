"""
 task to register user on stripe side
"""
import os

import djstripe
import stripe
from celery import shared_task, Celery
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from accounts.models import User

from subscriptions.models import Membership, UserMembership, UserSubscription

app = Celery('marketplace', broker='redis://localhost:6379/0')


# run this task to make user's accounts on stripe
@shared_task
def register_user_on_stripe():
    try:
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        user_email = User.objects.all()
        for user in user_email:
            user = get_object_or_404(User, email=user.email)
            user = get_object_or_404(User, email=user.email, membership_plan__customer__id=None)

            stripe_customer = stripe.Customer.create(
                email=user.email
            )
            stripe_subscription = stripe.Subscription.create(
                customer=stripe_customer["id"],
                items=[{'price': os.getenv('Free_Product_ID')}],

            )
            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(stripe_customer)
            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(stripe_subscription)

            user_membership = UserMembership.objects.filter(user=user).update(

                customer=djstripe_customer,

            )
            UserSubscription.objects.filter(user_membership=user_membership).update(
                stripe_subscription_id=stripe_subscription["id"]
                , subscription=djstripe_subscription)
    except Exception as e:
        print(e)


#
# @shared_task
# def single_register_user_on_stripe(email):
#     stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
#     user = User.objects.get(email=email)
#
#     # create stripe customer
#     stripe_customer = stripe.Customer.create(
#         email=user.email
#     )
#     print(stripe_customer)
#     # rdb.set_trace(stripe_customer)
#     # data = stripe.Customer.retrieve(id=stripe_customer['id'])
#     # if data['email'] == email:
#     #     return None
#     #
#     # else:
#     # sync data with dj-stripe
#     djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(stripe_customer)
#
#     print(djstripe_customer)
#     # rdb.set_trace()
#     user.customer = djstripe_customer
#
#     stripe_subscription = stripe.Subscription.create(
#         customer=stripe_customer["id"],
#         items=[{'price': 'price_1J58GBI4e8u2GP8qTZSw4HSi'}],
#
#     )
#
#     # sync data with subscription dj stripe
#     djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(stripe_subscription)
#
#     # user.subscription = djstripe_subscription
#     # subscription = UserSubscription.objects.create(
#     #     user_membership=user_membership,
#     #     active=stripe_subscription["status"],
#     #     stripe_subscription_id=stripe_subscription["id"]
#     #
#     # )
#     # subscription.save()
#     user.subscription = djstripe_subscription
#     print("done")
#     # user.save()


@shared_task
def register_user_on_stripe_no_customer_id():
    try:
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        user_email = User.objects.filter(membership_plan__customer__id=None)
        for user in user_email:
            user = get_object_or_404(User, email=user.email)
            stripe_customer = stripe.Customer.create(
                email=user.email
            )
            stripe_subscription = stripe.Subscription.create(
                customer=stripe_customer["id"],
                items=[{'price': os.getenv('Free_Product_ID')}],

            )
            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(stripe_customer)
            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(stripe_subscription)

            user_membership = UserMembership.objects.filter(user=user).update(

                customer=djstripe_customer,

            )
            UserSubscription.objects.filter(user_membership=user_membership).update(
                stripe_subscription_id=stripe_subscription["id"]
                , subscription=djstripe_subscription)
    except Exception as e:
        print(e)


@shared_task
def send_email_after_subscription(data):
    email_template_html = 'users/emails/send_subscription_message.html'
    sender = '"Digitvl" <noreply.digitvlhub@gmail.com>'
    headers = {'Reply-To': 'noreply.digitvlhub@gmail.com'}
    mail_subject = "Subscription Successfully"
    html_message = get_template(email_template_html)
    body = 'Thank you for upgrading to a DIGITVL Priemiere Artist, Included in this monthly subscription are the following' \
           '- Unlimited upload time for your audio uploads' \
           '- A DIGTVL Priemiere verified badge that will highlight your profile throughout the platform' \
           '- The ability to accept artist donations on your profile (coming soon)' \
           '- Have your music added to our DIGITVL playlist which opens opportunities to get placements in TV, Ads, Movies and More'
    template_context = {
        'username': data['username']
    }
    html_content = html_message.render(template_context)
    email = EmailMultiAlternatives(
        subject=mail_subject, body=body, from_email=sender, to=[data['email']], headers=headers
    )
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=True)
