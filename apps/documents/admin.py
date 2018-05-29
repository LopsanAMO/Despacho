from django.contrib import admin
from .models import UserClient, FolderClient, Document, Log


@admin.register(UserClient)
class UserClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'slug')
    list_filter = ('created',)


@admin.register(FolderClient)
class FolderClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created')
    list_filter = ('user', 'created')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder', 'created')
    list_filter = ('folder', 'created')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'updated')
    list_filter = ('user', 'action', 'updated')
