# Generated by Django 2.1.7 on 2019-03-05 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190305_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='pontoturistico',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='pontos_turisticos'),
        ),
    ]
