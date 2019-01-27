# Generated by Django 2.1.5 on 2019-01-24 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20190123_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(blank=True, choices=[('op', 'open'), ('cf', 'Confirmed'), ('cp', 'Complete')], default='op', help_text='Request Status', max_length=2),
        ),
    ]
