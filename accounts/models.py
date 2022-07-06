from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from common.timestamp import BaseTimestampModel
from django.utils.translation import gettext_lazy as _


# Custom User Manager for email field login
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        email = self.normalize_email(email)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """creates new super user with details """

        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(verbose_name=_('email'), max_length=255, unique=True)
    is_premium = models.BooleanField(verbose_name=_("Premium"), default=False)
    is_student = models.BooleanField(verbose_name=_('is student'), default=False)
    is_teacher = models.BooleanField(verbose_name=_('is teacher'), default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.first_name or self.username


class Student(BaseTimestampModel):
    user = models.OneToOneField(User, related_name='student_user', on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(max_length=1000)
    qualification = models.CharField(max_length=255, help_text='your qualification?')
    city = models.CharField(verbose_name=_('City'), max_length=255)

    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')

    def __str__(self):
        return self.user.first_name


class Teacher(BaseTimestampModel):
    user = models.OneToOneField(User, related_name='teacher_user', on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(verbose_name=_('City'), max_length=255)
    description = models.TextField(max_length=1000)
    qualification = models.CharField(max_length=255, help_text='your qualification?')
    upload_cv = models.FileField(upload_to='upload/cv/')

    class Meta:
        verbose_name = _('Teacher')
        verbose_name_plural = _('Teachers')

    def __str__(self):
        return self.user.first_name
