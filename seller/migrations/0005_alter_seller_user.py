# Generated by Django 4.0 on 2023-03-21 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_address_country'),
        ('seller', '0004_remove_seller_shop_picture_alter_seller_bank_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='account.user'),
        ),
    ]