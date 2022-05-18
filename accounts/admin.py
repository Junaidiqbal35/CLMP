from django.contrib import admin

# Register your models here.
from accounts.models import Student, Teacher, User

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)