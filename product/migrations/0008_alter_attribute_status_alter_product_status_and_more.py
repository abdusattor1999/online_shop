# Generated by Django 4.0 on 2023-03-30 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_productattribute_attribute_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='status',
            field=models.CharField(choices=[('inactive', 'inactive'), ('active', 'active')], default='active', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('inactive', 'inactive'), ('active', 'active')], default='active', max_length=30),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='status',
            field=models.CharField(choices=[('inactive', 'inactive'), ('active', 'active')], default='active', max_length=30),
        ),
    ]
