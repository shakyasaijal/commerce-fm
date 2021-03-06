# Generated by Django 3.0 on 2020-10-16 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DeliverySystem', '0001_initial'),
        ('OrderAndDelivery', '0013_auto_20201016_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_delivery_person', to='DeliverySystem.DeliveryPerson'),
        ),
        migrations.AlterField(
            model_name='order',
            name='direct_assign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_assigned', to='DeliverySystem.DeliveryPerson'),
        ),
    ]
