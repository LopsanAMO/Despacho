# Generated by Django 2.0.3 on 2018-03-19 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20180317_0711'),
    ]

    operations = [
        migrations.AddField(
            model_name='userclient',
            name='active',
            field=models.BooleanField(
                default=True,
                verbose_name='Cliente activo'),
        ),
    ]
