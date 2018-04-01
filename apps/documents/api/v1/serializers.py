from rest_framework import serializers
from documents.models import UserClient, FolderClient, Document


class DocumentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'document', 'folder')


class DocumentDetailSerializer(serializers.ModelSerializer):
    document = serializers.CharField()

    class Meta:
        model = Document
        fields = ('name', 'created', 'document', 'folder')
        depth = 1
        extra_kwargs = {'created': {'read_only': True}}


class DocumentSerializer(serializers.ModelSerializer):
    document = serializers.CharField()

    class Meta:
        model = Document
        fields = ('name', 'created', 'document')


class AllFolderClientSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = FolderClient
        fields = ('name', 'documents')

    def get_documents(self, obj):
        return DocumentSerializer(
            Document.objects.filter(folder__id=obj.id), many=True).data


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderClient
        fields = ('name', 'created', 'slug', 'user')
        extra_kwargs = {'created': {'read_only': True}, 'users': {'write_only': True}}


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
    url = serializers.SerializerMethodField()

    class Meta:
        model = UserClient
        fields = ('name', 'url')

    def get_url(self, obj):
        return '{}'.format(obj.slug)


class ClientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClient
        fields = ('name', 'id')


class ClientFolderSerializer(serializers.ModelSerializer):
    folders = serializers.SerializerMethodField()

    class Meta:
        model = UserClient
        fields = ('name', 'folders')

    def get_folders(self, obj):
        return FolderSerializer(
            FolderClient.objects.filter(user=obj), many=True).data
