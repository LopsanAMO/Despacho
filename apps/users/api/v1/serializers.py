import rest_auth.serializers
from rest_framework import serializers
from users.models import User
from utils.helpers import ErrorMesages


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        ErrorMesages().validate_email(value)
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        for key, value in ret.items():
            if value is None:
                ret[key] = ''
        return ret


class LoginSerializer(rest_auth.serializers.LoginSerializer):
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        fields['email'] = fields['username']
        del fields['username']
        return fields
