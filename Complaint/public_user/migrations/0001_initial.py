# Generated by Django 2.2.5 on 2021-04-11 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SuperAdmin', '0002_ministry_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(verbose_name='Location')),
                ('image', models.ImageField(upload_to='', verbose_name='Location Image')),
                ('note', models.TextField(verbose_name='Note')),
                ('ministry_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SuperAdmin.Ministry', verbose_name='Ministry Name')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
