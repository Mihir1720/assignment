# Generated by Django 4.2.3 on 2023-07-28 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_customuser_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
