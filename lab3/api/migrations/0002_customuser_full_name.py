# Generated by Django 4.2.5 on 2023-12-22 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(default='', max_length=50, verbose_name='ФИО'),
        ),
    ]
