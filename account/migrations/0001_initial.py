# Generated by Django 3.1.5 on 2021-08-08 13:32

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='uuid')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('nurse', 'Nurse'), ('pharmacist', 'Pharmacist'), ('laboratorist', 'Laboratorist'), ('accountant', 'Accountant'), ('admin', 'Admin')], default='patient', max_length=25, verbose_name='Category type of the user')),
                ('firstname', models.CharField(max_length=50, null=True)),
                ('lastname', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=25, null=True)),
                ('state', models.CharField(max_length=25, null=True)),
                ('country', models.CharField(max_length=25, null=True)),
                ('profile_image', models.ImageField(default=account.models.default_profile, max_length=255, null=True, upload_to=account.models.upload_to_profile, verbose_name='profile image')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Account of profile')),
            ],
        ),
    ]
