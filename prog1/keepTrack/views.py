from django.http.response import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect,HttpResponseBadRequest
from requests.api import request
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import *
from .serializers import *
from .CONFIG import auth_pa
from . import models
from rest_framework.decorators import action
import json
import requests
from rest_framework import generics
from rest_framework import status

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    @action(methods=['GET'], detail = False, url_path='projects',url_name='user-projects')
    def user_projects(self,request):
        if(request.user.is_authenticated):
            project_data = ProjectCardSerializer(request.user.projects.all(), many = True)
            # card_data = CardSerializer(request.user.cards.all(),many = True)
            return Response(project_data.data)
        else:
            return HttpResponseForbidden()
    
    @action(methods=['GET'], detail = False, url_path='cards',url_name='user-cards')
    def user_cards(self,request):
        if(request.user.is_authenticated):
            project_data = CardProjectSerializer(request.user.cards.all(), many = True)
            # card_data = CardSerializer(request.user.cards.all(),many = True)
            return Response(project_data.data)
        else:
            return HttpResponseForbidden()
    
    @action(methods=['GET'], detail = False, url_path='comments',url_name='user-comments')
    def user_comments(self,request):
        if(request.user.is_authenticated):
            comments_by_user = CommentCSerializer(request.user.comment_user.all(), many = True)
            return Response(comments_by_user.data)
        else:
            return HttpResponseForbidden()
    
    @action(methods=['GET'], detail = False, url_path='info',url_name='user-info')
    def user_self_info(self,request):
        if(request.user.is_authenticated):
            info = UserSerializer(request.user)
            return Response(info.data)
        else:
            return HttpResponseForbidden()

    @action(methods=['GET'], detail = False, url_path='logout',url_name='logout')
    def user_logout(self,request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'Logged out'})
        else:
            return HttpResponseForbidden()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [IsAdmin]
        elif self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = [NobodyCan]

        return super(UserViewSet, self).get_permissions()

class ProjectsOfAUser(APIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def get(self, request, pk ,format=None):
        user = Users.objects.get(id=pk)
        user_data = CardProjectSerializer(user.cards.all(), many = True)
        return Response(user_data.data)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def perform_create(self,serializer):
       serializer.save(creator = self.request.user)
    
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = []
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
                self.permission_classes = [IsAdminOrProjectAdmin]

        return super(ProjectViewSet, self).get_permissions()

class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = ListProjectSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            self.permission_classes = [IsAdminOrTeamMember_l]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAdminOrTeamMember]

        return super(ListViewSet, self).get_permissions()

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardProjectSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = []
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            self.permission_classes = [IsAdminOrTeamMember_c]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAdminOrTeamMember_l]

        return super(CardViewSet, self).get_permissions()

class ListOfProjects(APIView):

    def get(self, request, pk ,format=None):
        proj = Project.objects.get(id=pk)
        serializer = ListProjectSerializer(List.objects.filter(project_l = proj))
        return Response(serializer.data)

class CardsOfLists(APIView):

    def get(self, request, pk ,format=None):
        list = List.objects.get(id=pk)
        serializer = CardProjectSerializer(Card.objects.filter(list_c=list))
        return Response(serializer.data)

class CommentPViewSet(viewsets.ModelViewSet):
    queryset = Comment_p.objects.all()
    serializer_class = CommentPSerializer

    def perform_create(self,serializer):
        serializer.save(sender = self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = []
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [CommentEdit]
        elif self.request.method == 'DELETE' :
            self.permission_classes = [CommentPDelete]

        return super(CommentPViewSet, self).get_permissions()

class CommentCViewSet(viewsets.ModelViewSet):
    queryset = Comment_c.objects.all()
    serializer_class = CommentCSerializer

    def perform_create(self,serializer):
        serializer.save(sender = self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = []
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [CommentEdit]
        elif self.request.method == 'DELETE' :
            self.permission_classes = [CommentCDelete]

        return super(CommentCViewSet, self).get_permissions()










def oauth_redirect(req):
    url = f"https://channeli.in/oauth/authorise/?client_id={auth_pa['CLIENT_ID']}&redirect_uri={auth_pa['REDIRECT_URI']}&state={auth_pa['STATE_STRING']}"
    return HttpResponseRedirect(url)


def oauth_fetch_data(req):
    try:
        auth_code = req.GET['code']
    except:
        return HttpResponseBadRequest()
    parameters = {
        'client_id':auth_pa['CLIENT_ID'],
        'client_secret':auth_pa['CLIENT_SECRET'],
        'grant_type':'authorization_code',
        'redirect_uri':auth_pa['REDIRECT_URI'],
        'code':auth_code,
    }
    res = requests.post('https://channeli.in/open_auth/token/', data=parameters)

    if (res.status_code == 200):
        access_token=res.json()['access_token']
        refresh_token= res.json()['refresh_token']
    else:
        return HttpResponseBadRequest()

    header={
        "Authorization": "Bearer "+access_token,
    }
    res1 = requests.get("https://channeli.in/open_auth/get_user_data/", headers=header)
    
    data_stu = res1.json()

    isMaintainer = False

    for role in data_stu['person']['roles']:
        if role['role']=='Maintainer':
            isMaintainer = True
    if isMaintainer:
        try: 
            student = models.Users.objects.get(username = data_stu['username'])
        except models.Users.DoesNotExist:
            student = models.Users(
                username = data_stu['username'],
                name = data_stu['person']['fullName'],
                is_admin = False,
                details = 'Maintainer',
                banned = False
            )
            student.save()
        login(request=req, user = student)
        return HttpResponse("chalo login hogaya!!")
    else : 
        HttpResponse("This app can only be accessed by IMG members :p")
    return HttpResponse("hi") 