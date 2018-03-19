# Generated by Django 2.0.3 on 2018-03-17 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0004_folderclient_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentmodification',
            name='user',
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='Usuario que modifico'),
        ),
        migrations.AlterField(
            model_name='userclientmodification',
            name='user',
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name='Usuario'),
        ),
    ]
