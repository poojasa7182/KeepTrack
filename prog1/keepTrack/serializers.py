'''Serializers for keepTrack.models'''
from rest_framework import serializers
from keepTrack.models import *

class UserSerializer(serializers.ModelSerializer):
    '''User serializer'''
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields=['username','name','details']

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
    sender = UserSerializer()
    
    class Meta:
        model = Comment_p
        fields = '__all__'
        read_only_fields = ['sender','time']

class CommentCSerializer(serializers.ModelSerializer):
    '''Comment Serializer'''
    
    class Meta:
        model = Comment_c
        fields = '__all__'

class CommentCUserSerializer(serializers.ModelSerializer):
    '''Comment Serializer'''
    sender = UserSerializer()

    class Meta:
        model = Comment_c
        fields = '__all__'

class ProjectCardSerializer(serializers.ModelSerializer):
    card = CardSerializer(many=True, read_only = True)
    # list = ListSerializer(many = True , read_only = True)
    class Meta:
        model = Project
        fields = ['project_name','card','id', 'wiki', 'is_completed']
        read_only_fields = ['card']

class CardProjectSerializer(serializers.ModelSerializer):
    project_c = ProjectSerializer()
    list_c  = ListSerializer()
    # list = ListSerializer(many = True , read_only = True)
    class Meta:
        model = Card
        fields = ['id','card_name','list_c','start_date','due_date','is_completed','project_c','members_c','description']

class ListProjectSerializer(serializers.ModelSerializer):
    cardsOfList = CardSerializer(many=True, read_only = True)
    class Meta:
        model = List
        fields = ['id','list_name','project_l','is_completed','cardsOfList']


# class CardListProjectSerializer(serializers.ModelSerializer):
#     card = ProjectSerializer(many=True)
#     class Meta:
#         model = Card
#         fields = ['card_name','list_c','start_date','due_date','is_completed','project_c','members_c','description','tags_c','card']