from django.db import models
from datetime import datetime
from users.models import User


class UserClient(models.Model):
    name = models.CharField(blank=True, max_length=100)
    created = models.DateTimeField(blank=True, default=datetime.now)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class FolderClient(models.Model):
    user = models.OneToOneField(UserClient, on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=100)
    created = models.DateTimeField(blank=True, default=datetime.now)

    @property
    def folder_name(self):
        return "Folder de {}".format(self.user.name)

    def __str__(self):
        return "{}".format(self.folder_name)

    class Meta:
        verbose_name = 'Folder de Cliente'
        verbose_name_plural = 'Folders de Clientes'


class UserClientModification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_folder = models.ForeignKey(FolderClient, on_delete=models.CASCADE)
    updated = models.DateTimeField(
        blank=True,
        auto_now_add=True
    )

    def __str__(self):
        return "Modificacion al {}".format(self.folder_name)

    class Meta:
        verbose_name = 'Modificacion de Folder'
        verbose_name_plural = 'Modificaciones de Folders'


class Document(models.Model):
    folder = models.ForeignKey(FolderClient, on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=100)
    created = models.DateTimeField(blank=True, default=datetime.now)

    def __str__(self):
        return "Documento: {} del folder {}".foormat(
            self.name,
            self.folder.folder_name
        )

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
