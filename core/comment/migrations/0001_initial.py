# Generated by Django 3.2.25 on 2024-09-12 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0005_auto_20240904_1106'),
        ('blog', '0006_alter_post_published_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='accounts.profile')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]