# Generated by Django 4.0.4 on 2022-07-02 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0015_rename_rate_comment_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='video_watched',
            field=models.BooleanField(default=False),
        ),
    ]
