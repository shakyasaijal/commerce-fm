# Generated by Django 3.0 on 2020-10-16 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderAndDelivery', '0007_paymentmethods'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmethods',
            name='count',
            field=models.BigIntegerField(default=0),
        ),
    ]
