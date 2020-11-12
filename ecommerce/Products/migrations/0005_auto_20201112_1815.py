# Generated by Django 3.0 on 2020-11-12 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Offer', '0003_offer_discounts'),
        ('Products', '0004_newcategoryrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='offer_category',
            field=models.ManyToManyField(blank=True, related_name='offer_category', to='Offer.OfferCategory'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='offers',
        ),
        migrations.AddField(
            model_name='product',
            name='offers',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_products', to='Offer.Offer'),
        ),
    ]