# Generated by Django 4.0.4 on 2022-06-28 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_category_category_image_course_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_image',
            field=models.URLField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='course',
            name='course_image',
            field=models.URLField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
