# Generated by Django 5.1.3 on 2024-11-10 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0003_redeemeditem_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='redeemeditem',
            old_name='reward_id',
            new_name='reward',
        ),
    ]
