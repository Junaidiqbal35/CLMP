# Generated by Django 4.0.4 on 2022-07-02 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0017_remove_content_video_watched'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseprogress',
            name='content',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='content_progress', to='courses.content'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='courseprogress',
            name='visited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='courseprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_content_progress', to=settings.AUTH_USER_MODEL),
        ),
    ]
