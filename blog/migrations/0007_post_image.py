# Generated by Django 3.1.1 on 2020-10-01 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201001_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_photos/%Y/%m/%d/'),
        ),
    ]
