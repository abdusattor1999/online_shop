# Generated by Django 4.0 on 2023-05-27 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_product_view_alter_product_attributes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(blank=True, null=True, to='product.AttributeValue'),
        ),
    ]