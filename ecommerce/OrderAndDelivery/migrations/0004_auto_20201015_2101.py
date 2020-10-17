# Generated by Django 3.0 on 2020-10-15 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CartSystem', '0003_auto_20201011_1753'),
        ('OrderAndDelivery', '0003_auto_20201011_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='vendor',
        ),
        migrations.AddField(
            model_name='order',
            name='deliver_to',
            field=models.BooleanField(choices=[(True, 'Self'), (False, 'Other')], default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='district',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CartSystem.Location'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='other_address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='other_full_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='other_phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_by',
            field=models.BooleanField(choices=[(True, 'Self'), (False, 'Other')], default=True),
        ),
        migrations.DeleteModel(
            name='Delivery',
        ),
    ]
