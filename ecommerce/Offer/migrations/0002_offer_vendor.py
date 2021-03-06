# Generated by Django 3.0 on 2020-10-11 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Offer', '0001_initial'),
        ('Vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='vendor',
            field=models.ManyToManyField(help_text='Which vendors can participate?', related_name='vendors_offer', to='Vendor.Vendor'),
        ),
    ]
