from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from api.models import Snippet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        User.objects.create_user(**validated_data)
        return validated_data


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ('id', 'code', 'language', 'owner')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.code = validated_data.get('code', instance.code)
        instance.language = validated_data.get('language', instance.language)
        instance.created = timezone.now()
        instance.save()
        return instance


class OverallScoreboardSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    rank = serializers.IntegerField()
