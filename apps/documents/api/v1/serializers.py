from restframework import serializers
from documents.models import UserClient, FolderClient, Document


class UserClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClient
        fields = ('name', 'created')
        extra_kwargs = {
            'created': {
                'read_only': True
            }
        }


class FolderClient(serializers.ModelSerializer):
    user =

    class Meta:
        model = FolderClient
        fields = ('user', 'name', 'created')
        extra_kwargs = {
            'created': {
                'read_only': True
            }
        }
