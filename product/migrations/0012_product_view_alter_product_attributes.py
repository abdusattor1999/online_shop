# Generated by Django 4.0 on 2023-04-28 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_product_attributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='view',
            field=models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni"),
        ),
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(blank=True, to='product.AttributeValue'),
        ),
    ]
