# Generated by Django 2.0.3 on 2018-03-14 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, verbose_name='Nombre del documento')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
            },
        ),
        migrations.CreateModel(
            name='DocumentModification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de modificacion')),
                ('document', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='documents.Document', verbose_name='Documento')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario que modifico')),
            ],
            options={
                'verbose_name': 'Documento Modificado',
                'verbose_name_plural': 'Documentos modificados',
            },
        ),
        migrations.CreateModel(
            name='FolderClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, verbose_name='Nombre de Folder')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
            ],
            options={
                'verbose_name': 'Folder de Cliente',
                'verbose_name_plural': 'Folders de Clientes',
            },
        ),
        migrations.CreateModel(
            name='UserClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, verbose_name='Nombre del Cliente')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='UserClientModification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de modificacion')),
                ('user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('user_folder', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='documents.FolderClient', verbose_name='Folder de usuario')),
            ],
            options={
                'verbose_name': 'Modificacion de Folder',
                'verbose_name_plural': 'Modificaciones de Folders',
            },
        ),
        migrations.AddField(
            model_name='folderclient',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='documents.UserClient', verbose_name='Cliente'),
        ),
        migrations.AddField(
            model_name='document',
            name='folder',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='documents.FolderClient', verbose_name='Folder del cliente'),
        ),
    ]
