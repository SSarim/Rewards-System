# Generated by Django 5.1.3 on 2024-11-10 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redeemeditem',
            name='item_code',
            field=models.CharField(max_length=16, null=True, unique=True),
        ),
    ]
