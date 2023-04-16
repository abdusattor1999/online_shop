# Generated by Django 4.0 on 2023-04-15 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_attribute_status_alter_product_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('inactive', 'inactive'), ('active', 'active')], default='active', max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='value',
        ),
        migrations.AlterField(
            model_name='attribute',
            name='status',
            field=models.CharField(choices=[('inactive', 'inactive'), ('active', 'active')], default='active', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('inactive', 'inactive'), ('active', 'active')], default='active', max_length=60),
        ),
        migrations.DeleteModel(
            name='ProductAttribute',
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='attribute',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='product.attribute'),
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(blank=True, to='product.AttributeValue'),
        ),
    ]
