from rest_framework import serializers
from documents.models import UserClient, FolderClient, Document

class DocumentSerializer(serializers.ModelSerializer):
    document = serializers.CharField()

    class Meta:
        model = Document
        fields = ('name', 'created', 'document')


class AllFolderClientSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()

    class Meta:
        model = FolderClient
        fields = ('name', 'document')

    def get_document(self, obj):
        return DocumentSerializer(
            Document.objects.filter(folder__id=obj.id), many=True).data


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderClient
        fields = ('name', 'created')


class AllUserClientSerializer(serializers.ModelSerializer):
    folder = serializers.SerializerMethodField()

    class Meta:
        model = UserClient
        fields = ('name', 'created', 'folder')
        extra_kwargs = {
            'created': {
                'read_only': True
            }
        }

    def get_folder(self, obj):
        return AllFolderClientSerializer(
            FolderClient.objects.filter(user=obj), many=True).data


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClient
        fields = ('name', )


class ClientFolderSerializer(serializers.ModelSerializer):
    folders = serializers.SerializerMethodField()

    class Meta:
        model = UserClient
        fields = ('name', 'folders')

    def get_folders(self, obj):
        return FolderSerializer(
            FolderClient.objects.filter(user=obj), many=True).data
