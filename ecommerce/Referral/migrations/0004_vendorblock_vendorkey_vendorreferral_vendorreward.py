# Generated by Django 3.0 on 2020-10-11 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0001_initial'),
        ('Referral', '0003_block_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorReferral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('refer_code', models.CharField(max_length=255)),
                ('refer_url', models.URLField(default='')),
                ('vendor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Vendor.Vendor')),
            ],
            options={
                'verbose_name': 'Vendor Referral Activation',
                'verbose_name_plural': 'Vendor Referral Activations',
            },
        ),
        migrations.CreateModel(
            name='VendorReward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('points', models.BigIntegerField(default=0)),
                ('visited', models.BigIntegerField(default=0)),
                ('signed_up', models.BigIntegerField(default=0)),
                ('buyed', models.BigIntegerField(default=0)),
                ('referral', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Referral.VendorReferral')),
            ],
            options={
                'verbose_name': 'Vendor Reward',
                'verbose_name_plural': 'Vendor Rewards',
            },
        ),
        migrations.CreateModel(
            name='VendorKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=255, unique=True)),
                ('referredFrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Referral.VendorReferral')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VendorBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', models.CharField(max_length=255)),
                ('data_hash', models.CharField(max_length=255, unique=True)),
                ('previous_has', models.TextField(default='00xx00')),
                ('genesis_block', models.BooleanField(choices=[(True, 'Is a Genesis Block.'), (False, 'Is not a Genesis Block.')], default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Vendor.Vendor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]