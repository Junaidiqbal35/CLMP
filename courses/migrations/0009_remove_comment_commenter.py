# Generated by Django 4.0.4 on 2022-06-16 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_remove_comment_course_video_comment_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='commenter',
        ),
    ]