# Generated by Django 5.1.3 on 2024-11-05 17:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('reward_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('points_earned', models.IntegerField()),
                ('points_redeemed', models.IntegerField()),
                ('reward_description', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('earned_date', models.DateTimeField(blank=True, null=True)),
                ('redeemed_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RedeemedItem',
            fields=[
                ('item_code', models.CharField(max_length=16, unique=True)),
                ('reward_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='rewards.reward')),
                ('item_description', models.CharField(max_length=255)),
            ],
        ),
    ]