# Generated by Django 3.0 on 2020-10-11 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Products', '0001_initial'),
        ('OrderAndDelivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.Product'),
        ),
    ]
