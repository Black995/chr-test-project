# Generated by Django 4.1.7 on 2023-02-16 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_extra_location_network_station_delete_bike_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra',
            name='station',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='station_extra', to='tasks.station'),
        ),
        migrations.AlterField(
            model_name='network',
            name='location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='location_network', to='tasks.location'),
        ),
        migrations.AlterField(
            model_name='station',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='network_station', to='tasks.network'),
        ),
    ]
