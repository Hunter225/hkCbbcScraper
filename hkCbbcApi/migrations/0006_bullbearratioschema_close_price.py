# Generated by Django 3.0.8 on 2020-07-30 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hkCbbcApi', '0005_auto_20200729_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='bullbearratioschema',
            name='close_price',
            field=models.FloatField(null=True),
        ),
    ]
