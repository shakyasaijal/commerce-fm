# Generated by Django 3.0 on 2020-10-11 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', models.CharField(max_length=255)),
                ('data_hash', models.CharField(max_length=255, unique=True)),
                ('previous_has', models.TextField(default='00xx00')),
                ('genesis_block', models.BooleanField(choices=[(True, 'Is a Genesis Block.'), (False, 'Is not a Genesis Block.')], default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('refer_code', models.CharField(max_length=255)),
                ('refer_url', models.URLField(default='')),
            ],
            options={
                'verbose_name': 'Referral Activation',
                'verbose_name_plural': 'Referral Activations',
            },
        ),
        migrations.CreateModel(
            name='UserKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=255, unique=True)),
                ('referredFrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Referral.Referral')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('points', models.BigIntegerField(default=0)),
                ('visited', models.BigIntegerField(default=0)),
                ('signed_up', models.BigIntegerField(default=0)),
                ('buyed', models.BigIntegerField(default=0)),
                ('referral', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Referral.Referral')),
            ],
            options={
                'verbose_name': 'Reward',
                'verbose_name_plural': 'Rewards',
            },
        ),
    ]
