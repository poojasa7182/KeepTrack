'''Serializers for keepTrack.models'''
from rest_framework import serializers
from keepTrack.models import *

class UserSerializer(serializers.ModelSerializer):
    '''User serializer'''
    class Meta:
        model = Users
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    '''Project Serializer'''
    class Meta:
        model = Project
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    '''List Serilizer'''
    class Meta:
        model = List
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    '''Card Serializer'''
    class Meta:
        model = Card
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    '''Comment Serializer'''
    class Meta:
        model = Comment
        fields = '__all__'