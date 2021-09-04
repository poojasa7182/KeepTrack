from django.http.response import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect,HttpResponseBadRequest
from requests.api import request
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
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
            comments_by_user = CommentSerializer(request.user.comment_user.all(), many = True)
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

# class AdminViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAdmin]

#     def all_users(self,request):
#         users = Users.objects.all()
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(methods=['GET'], detail = False, url_path='allProjects',url_name='project-allProjects')
    def listAllProg(self,request):
        if(request.user.is_authenticated):
            proj = Project.objects.all()
            projectsAll = ProjectSerializer(proj,many=True)
            return Response(projectsAll.data)
        else:
            return HttpResponseForbidden()
    
    @action(methods=['POST'], detail = False, url_path='mkProject',url_name='project-mkProject')
    def mkProj(self,request):
        if(request.user.is_authenticated):
            proj = ProjectSerializer(data=request.data)
            
            if proj.is_valid():
                proj.save(creator= request.user)
                print(proj.validated_data.get({'members_p'}))
                proj.save()

                return Response(proj.data,status=status.HTTP_201_CREATED)
            return Response(proj.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponseForbidden()



# class ProjectDetailSet(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]



    









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