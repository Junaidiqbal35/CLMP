from django.contrib import admin

# Register your models here.
from .models import Membership, UserMembership, UserSubscription


class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'membership', 'volume_remaining')
    search_fields = ['user__email']


admin.site.register(Membership)
admin.site.register(UserSubscription)
admin.site.register(UserMembership, UserMembershipAdmin)
