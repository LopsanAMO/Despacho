from django.db import models
from datetime import datetime
from users.models import User


class UserClient(models.Model):
    name = models.CharField(
        verbose_name='Nombre del Cliente',
        blank=True,
        max_length=150
    )
    created = models.DateTimeField(
        verbose_name='Fecha de creacion',
        blank=True,
        auto_now_add=True
    )

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class FolderClient(models.Model):
    user = models.OneToOneField(
        UserClient,
        verbose_name='Cliente',
        blank=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Nombre de Folder',
        blank=True,
        max_length=150
    )
    created = models.DateTimeField(
        verbose_name='Fecha de creacion',
        blank=True,
        auto_now_add=True
    )

    @property
    def folder_name(self):
        return "Folder de {}".format(self.user.name)

    def __str__(self):
        return "{}".format(self.folder_name)

    class Meta:
        verbose_name = 'Folder de Cliente'
        verbose_name_plural = 'Folders de Clientes'


class UserClientModification(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name='Usuario',
        blank=True,
        on_delete=models.CASCADE
    )
    user_folder = models.ForeignKey(
        FolderClient,
        verbose_name='Folder de usuario',
        blank=True,
        on_delete=models.CASCADE
    )
    updated = models.DateTimeField(
        verbose_name='Fecha de modificacion',
        blank=True,
        auto_now_add=True
    )

    def __str__(self):
        return "Modificacion al {}".format(self.folder_name)

    class Meta:
        verbose_name = 'Modificacion de Folder'
        verbose_name_plural = 'Modificaciones de Folders'


class Document(models.Model):
    folder = models.ForeignKey(
        FolderClient,
        verbose_name='Folder del cliente',
        blank=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Nombre del documento',
        blank=True,
        max_length=150
    )
    created = models.DateTimeField(
        verbose_name='Fecha de creacion',
        blank=True,
        auto_now_add=True
    )
    document = models.FileField(
        verbose_name='Documento',
        upload_to='documents/',
        null=True,
        blank=True
    )

    def __str__(self):
        return "Documento: {} del folder {}".format(
            self.name,
            self.folder.folder_name
        )

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'


class DocumentModification(models.Model):
    document = models.ForeignKey(
        Document,
        verbose_name='Documento',
        blank=True,
        on_delete=models.CASCADE
    )
    user = models.OneToOneField(
        User,
        verbose_name='Usuario que modifico',
        blank=True,
        on_delete=models.CASCADE
    )
    updated = models.DateTimeField(
        verbose_name='Fecha de modificacion',
        blank=True,
        auto_now_add=True
    )

    def __str__(self):
        return "Documento modificado: {}".format(self.document.name)

    class Meta:
        verbose_name = 'Documento Modificado'
        verbose_name_plural = 'Documentos modificados'
