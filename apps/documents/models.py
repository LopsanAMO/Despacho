from django.db import models
from django.template import defaultfilters
from datetime import datetime
from users.models import User
from enum import Enum


class UserClient(models.Model):
    name = models.CharField(
        verbose_name='Nombre del Cliente',
        blank=True,
        max_length=150
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=50,
        null=True,
        blank=True,
        unique=True
    )
    created = models.DateTimeField(
        verbose_name='Fecha de creacion',
        blank=True,
        auto_now_add=True
    )
    active = models.BooleanField(
        verbose_name='Cliente activo',
        default=True
    )

    def save(self, *args, **kwargs):
        empty_list = ['', ' ', None]
        if self.slug in empty_list or self.slug != defaultfilters.slugify(self.name):  # noqa
            self.slug = defaultfilters.slugify(self.name)
        super(UserClient, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        unique_together = ('name',)


class FolderClient(models.Model):
    user = models.ForeignKey(
        UserClient,
        verbose_name='Cliente',
        blank=True,
        on_delete=models.CASCADE
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=100,
        null=True,
        blank=True,
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

    def save(self, *args, **kwargs):
        empty_list = ['', ' ', None]
        if self.slug in empty_list or self.slug != defaultfilters.slugify(self.name):  # noqa
            self.slug = defaultfilters.slugify(self.name)
        super(FolderClient, self).save(*args, **kwargs)

    @property
    def folder_name(self):
        return "Folder de {}: {}".format(self.user.name, self.name)

    def __str__(self):
        return "{}".format(self.folder_name)

    class Meta:
        verbose_name = 'Folder de Cliente'
        verbose_name_plural = 'Folders de Clientes'


class UserClientModification(models.Model):
    user = models.ForeignKey(
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
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=100,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "Documento: {} del folder {}".format(
            self.name,
            self.folder.folder_name
        )

    def save(self, *args, **kwargs):
        empty_list = ['', ' ', None]
        if self.slug in empty_list or self.slug != defaultfilters.slugify(self.name):  # noqa
            self.slug = defaultfilters.slugify(self.name)
        super(Document, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'


class Log(models.Model):
    class NOTIFICATION_TYPE(Enum):
        create_client = ('create_client', 'Cliente Creado')
        update_client = ('update_client', 'Cliente Actualizado')
        delete_client = ('delete_client', 'Cliente Eliminado')
        create_folder = ('create_folder', 'Folder Creado')
        update_folder = ('update_folder', 'Folder Actualizado')
        delete_folder = ('delete_folder', 'Folder Eliminado')
        create_document = ('create_document', 'Documento, Creado')
        update_document = ('update_document', 'Documento Actializado')
        delete_document = ('delete_Document', 'Documento Eliminado')

        @classmethod
        def get_value(cls, _type):
            try:
                return cls[_type].value[0]
            except KeyError:
                return ''

    action = models.CharField(
        verbose_name='Tipo de accion',
        choices=[x.value for x in NOTIFICATION_TYPE],
        null=False,
        blank=True,
        max_length=20
    )
    user = models.ForeignKey(
        User,
        verbose_name='Usuario',
        blank=True,
        on_delete=models.CASCADE
    )
    updated = models.DateTimeField(
        verbose_name='Fecha de modificacion',
        blank=True,
        auto_now_add=True
    )
    description = models.CharField(
        verbose_name='Descripcion',
        max_length=300,
        blank=True,
        null=True
    )

    def __str__(self):
        return '{} - {}'.format(self.user.email, self.action)

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
