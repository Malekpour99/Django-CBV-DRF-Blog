# Generated by Django 3.2.25 on 2024-07-25 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_auto_20240725_1011"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                default="default/default-post.png", upload_to="blog/"
            ),
        ),
    ]
