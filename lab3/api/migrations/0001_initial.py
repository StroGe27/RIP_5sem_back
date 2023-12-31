# Generated by Django 4.2.5 on 2023-12-22 16:47

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email адрес')),
                ('password', models.CharField(max_length=50, verbose_name='Пароль')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Является ли пользователь менеджером?')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Является ли пользователь админом?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', api.models.NewUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AvailableOS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'availableos',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'processor',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Requests_status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_status', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'requests_status',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_create', models.DateField()),
                ('date_formation', models.DateField()),
                ('date_complete', models.DateField()),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.requests_status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'db_table': 'requests',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=10)),
                ('processor', models.CharField(max_length=100)),
                ('ghz', models.FloatField()),
                ('ram', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('ip', models.CharField(max_length=20)),
                ('img', models.CharField(max_length=20)),
                ('availableos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.availableos')),
                ('processor_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.processor')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'db_table': 'orders',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Order_to_request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_months', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orders')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.requests')),
            ],
            options={
                'db_table': 'order_to_request',
                'managed': True,
            },
        ),
    ]
