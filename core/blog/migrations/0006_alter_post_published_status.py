# Generated by Django 3.2.25 on 2024-09-04 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_status',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]