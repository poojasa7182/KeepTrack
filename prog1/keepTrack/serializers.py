'''Serializers for keepTrack.models'''
from rest_framework import serializers
from keepTrack.models import *

class UserSerializer(serializers.ModelSerializer):
    '''User serializer'''
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields=['username','name','details']

# class UserProjectsSerializer(serializers.ModelSerializer):

class ProjectSerializer(serializers.ModelSerializer):
    '''Project Serializer'''
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields=['creator']

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

class CommentPSerializer(serializers.ModelSerializer):
    '''Comment Serializer'''
    class Meta:
        model = Comment_p
        fields = '__all__'
        read_only_fields = ['sender','time','project']

class CommentCSerializer(serializers.ModelSerializer):
    '''Comment Serializer'''
    class Meta:
        model = Comment_c
        fields = '__all__'
        read_only_fields = ['sender','time','card']

class ProjectCardSerializer(serializers.ModelSerializer):
    card = CardSerializer(many=True, read_only = True)
    # list = ListSerializer(many = True , read_only = True)
    class Meta:
        model = Project
        fields = ['project_name','card']
        read_only_fields = ['card']

class CardProjectSerializer(serializers.ModelSerializer):
    project_c = ProjectSerializer()
    list_c  = ListSerializer()
    # list = ListSerializer(many = True , read_only = True)
    class Meta:
        model = Card
        fields = ['card_name','list_c','start_date','due_date','is_completed','project_c','members_c','description','tags_c','card']

class ListProjectSerializer(serializers.ModelSerializer):
    project_l = ProjectSerializer()

    class Meta:
        model = List
        fields = ['list_name','project_l','start_date','due_date','is_completed','tags_l','members_l']


# class CardListProjectSerializer(serializers.ModelSerializer):
#     card = ProjectSerializer(many=True)
#     class Meta:
#         model = Card
#         fields = ['card_name','list_c','start_date','due_date','is_completed','project_c','members_c','description','tags_c','card']