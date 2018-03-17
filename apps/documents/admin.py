from django.contrib import admin
from .models import (
    UserClient, FolderClient, UserClientModification, Document,
    DocumentModification
)


@admin.register(UserClient)
class UserClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'slug')
    list_filter = ('created',)


@admin.register(FolderClient)
class FolderClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created')
    list_filter = ('user', 'created')


@admin.register(UserClientModification)
class UserClientModificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_folder', 'updated')
    list_filter = ('user', 'user_folder', 'updated')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder', 'created')
    list_filter = ('folder', 'created')


@admin.register(DocumentModification)
class DocumentModificationAdmin(admin.ModelAdmin):
    list_display = ('document', 'user', 'updated')
    list_filter = ('document', 'user', 'updated')
