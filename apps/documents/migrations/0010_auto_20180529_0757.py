# Generated by Django 2.0.3 on 2018-05-29 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0009_auto_20180402_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('action',
                 models.CharField(
                     blank=True,
                     choices=[
                         ('create_client',
                          'Cliente Creado'),
                         ('update_client',
                          'Cliente Actualizado'),
                         ('delete_client',
                          'Cliente Eliminado'),
                         ('create_folder',
                          'Folder Creado'),
                         ('update_folder',
                          'Folder Actualizado'),
                         ('delete_folder',
                          'Folder Eliminado'),
                         ('create_document',
                          'Documento, Creado'),
                         ('update_document',
                          'Documento Actializado'),
                         ('delete_Document',
                          'Documento Eliminado')],
                     max_length=20,
                     verbose_name='Tipo de accion')),
                ('updated',
                 models.DateTimeField(
                     auto_now_add=True,
                     verbose_name='Fecha de modificacion')),
                ('description',
                 models.CharField(
                     blank=True,
                     max_length=300,
                     null=True,
                     verbose_name='Descripcion')),
                ('user',
                 models.ForeignKey(
                     blank=True,
                     on_delete=django.db.models.deletion.CASCADE,
                     to=settings.AUTH_USER_MODEL,
                     verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Registro',
                'verbose_name_plural': 'Registros',
            },
        ),
        migrations.RemoveField(
            model_name='documentmodification',
            name='document',
        ),
        migrations.RemoveField(
            model_name='documentmodification',
            name='user',
        ),
        migrations.DeleteModel(
            name='DocumentModification',
        ),
    ]
