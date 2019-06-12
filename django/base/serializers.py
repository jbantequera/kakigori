from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedIdentityField(view_name='profile-detail', read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'url', 'profile')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')

    class Meta:
        model = Profile
        fields = ('display_name', 'bio', 'url', 'user')