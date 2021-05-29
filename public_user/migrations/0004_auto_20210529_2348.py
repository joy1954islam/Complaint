# Generated by Django 2.2.5 on 2021-05-29 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SuperAdmin', '0004_policestation_email'),
        ('public_user', '0003_complaint_is_next_update_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SuperAdmin.District', verbose_name='District'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='police_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SuperAdmin.PoliceStation', verbose_name='Police Station'),
        ),
    ]
