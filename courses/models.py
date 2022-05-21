from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
from django.db import models
from django.conf import settings

from courses.fields import OrderField


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Course(models.Model):
    COURSE_SUBSCRIPTION_TYPE = (
        (1, 'FREE'),
        (2, 'PREMIUM'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    category = models.ForeignKey(Category,
                                 related_name='courses',
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    subscription_package = models.PositiveIntegerField(choices=COURSE_SUBSCRIPTION_TYPE, default=1)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                      related_name='courses_joined',
                                      blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']


class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='content_owner',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    video = models.FileField(upload_to='courses/video/')

    # content_type = models.ForeignKey(ContentType,
    #                                  on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # item = GenericForeignKey('content_type', 'object_id')

    order = OrderField(blank=True, for_fields=['module'])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']


# class ItemBase(models.Model):
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL,
#                               related_name='%(class)s_related',
#                               on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True
#
#     def __str__(self):
#         return self.title
#
#
# class Text(ItemBase):
#     content = models.TextField()
#
#
# class File(ItemBase):
#     file = models.FileField(upload_to='files')
#
#
# class Image(ItemBase):
#     file = models.FileField(upload_to='images')
#
#
# class Video(ItemBase):
#     url = models.URLField()
