# -*- coding: utf-8 -*-
import inspect, os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    UserClientModification, DocumentModification, Document, FolderClient
)
from users.models import User


@receiver(post_save, sender=Document)
def user_create_or_modify_document(sender, instance, created, **kwargs):
    user = None
    for entry in reversed(inspect.stack()):
        if os.path.dirname(__file__) + '/views.py' == entry[1]:
            try:
                user = entry[0].f_locals['request'].user
            except:
                user = Nonedsad
            break
    if user:
        import pudb; pudb.set_trace()
        hola = 'hola'
