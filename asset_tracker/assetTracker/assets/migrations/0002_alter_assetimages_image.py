# Generated by Django 4.2.3 on 2023-08-02 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetimages',
            name='image',
            field=models.ImageField(upload_to='assetImages/'),
        ),
    ]
