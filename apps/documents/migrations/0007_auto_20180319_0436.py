# Generated by Django 2.0.3 on 2018-03-19 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_userclient_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folderclient',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='documents.UserClient', verbose_name='Cliente'),
        ),
    ]