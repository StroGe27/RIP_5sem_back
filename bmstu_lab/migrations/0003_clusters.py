# Generated by Django 4.2.6 on 2023-10-23 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu_lab', '0002_alter_orders_options_alter_requests_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clusters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
    ]
