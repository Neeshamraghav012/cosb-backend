# Generated by Django 4.1 on 2022-09-02 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_ratings'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ratings',
        ),
    ]
