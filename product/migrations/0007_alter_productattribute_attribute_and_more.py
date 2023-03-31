# Generated by Django 4.0 on 2023-03-30 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_attribute_status_alter_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='attribute',
            field=models.ManyToManyField(blank=True, to='product.Attribute'),
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='product',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_attributes', to='product.product'),
            preserve_default=False,
        ),
    ]