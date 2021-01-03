# Generated by Django 3.1.4 on 2020-12-31 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20201231_0442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='content',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='image',
        ),
        migrations.AddField(
            model_name='category',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
