# Generated by Django 4.0 on 2023-04-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_attributevalue_remove_attribute_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(blank=True, null=True, to='product.AttributeValue'),
        ),
    ]
