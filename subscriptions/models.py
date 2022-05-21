import os

import djstripe
import stripe
import logging
from django.db import models, transaction
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.
from django.shortcuts import get_object_or_404
from djstripe.models import Customer, Subscription


# Get an instance of a logger
logger = logging.getLogger(__name__)

MEMBERSHIP_CHOICES = (
    ('Standard', 'standard'),
    ('Free', 'free')
)


class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Free',
        max_length=30)
    price = models.IntegerField(default=0.0)

    stripe_plan_id = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='membership_plan', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    subscription_badge = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name

    @property
    def get_customer_id(self):
        return self.customer.id


def post_save_user_membership_create(sender, instance, created, *args, **kwargs):
    try:
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        with transaction.atomic():
            user_membership, created = UserMembership.objects.get_or_create(user=instance)
            if created:
                free_membership = get_object_or_404(Membership, membership_type='Free')
                user_membership.membership = free_membership

                # create stripe customer
                stripe_customer = stripe.Customer.create(
                    email=user_membership.user.email
                )

                djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(stripe_customer)

                user_membership.customer = djstripe_customer

                stripe_subscription = stripe.Subscription.create(
                    customer=stripe_customer["id"],
                    items=[{'price': os.getenv('Free_Product_ID')}],

                )

                # sync data with subscription dj stripe
                djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(stripe_subscription)

                subscription_data = djstripe_subscription
                subscription = UserSubscription.objects.create(
                    user_membership=user_membership,
                    stripe_subscription_id=stripe_subscription["id"],
                    subscription=subscription_data

                )
                subscription.save()
                user_membership.save()
                print("done")
    except Exception as e:
        logger.error(e)


post_save.connect(post_save_user_membership_create, sender=settings.AUTH_USER_MODEL,
                  dispatch_uid="subscriptions.models.post_save_user_membership_create")


class UserSubscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name="user_membership_subscription",
                                        on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, null=True, blank=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        return self.subscription.created

    @property
    def get_next_billing_date(self):
        return self.subscription.current_period_end

    @property
    def get_plan(self):
        return self.subscription.plan.product.name

    @property
    def get_payment_method(self):
        return self.subscription.default_payment_method
