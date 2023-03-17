# Generated by Django 4.0 on 2023-03-16 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_cofirmation_type_alter_uploadfile_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='user',
            new_name='profile',
        ),
        migrations.AlterField(
            model_name='cofirmation',
            name='type',
            field=models.CharField(choices=[('register', 'register'), ('resend', 'resend'), ('change_phone', 'change_phone'), ('password_reset', 'password_reset'), ('order', 'order')], default='register', max_length=20),
        ),
    ]
