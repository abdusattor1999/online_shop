# Generated by Django 4.0 on 2023-03-21 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_address_country'),
        ('seller', '0005_alter_seller_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.user'),
        ),
    ]
