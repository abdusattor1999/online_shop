# Generated by Django 4.0 on 2023-03-27 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImageProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='product_images/')),
            ],
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='image',
        ),
        migrations.AlterField(
            model_name='attribute',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=30),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=30),
        ),
        migrations.AddField(
            model_name='productimage',
            name='images',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.uploadimageproduct'),
        ),
    ]
