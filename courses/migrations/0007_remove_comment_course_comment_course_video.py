# Generated by Django 4.0.4 on 2022-05-25 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='course',
        ),
        migrations.AddField(
            model_name='comment',
            name='course_video',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='courses.content'),
            preserve_default=False,
        ),
    ]