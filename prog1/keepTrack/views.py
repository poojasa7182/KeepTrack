'''views '''
from django.http.response import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import  redirect, render
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
from rest_framework.decorators import api_view
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
from asgiref.sync import async_to_sync

class UserViewSet(viewsets.ModelViewSet):
    '''get user projects/cards/info/comments, login/logout'''
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsEnabeled]

    @action(methods=['GET'], detail = False, url_path='projects',url_name='user-projects')
    def user_projects(self,request):
        if(request.user.is_authenticated and not (request.user.banned)):
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
            comments_by_user = CommentCSerializer(request.user.commenter_c.all(), many = True)
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

    #@action(methods=['GET'], detail = False, url_path='login',url_name='user-login')
    

    @action(methods=['GET'], detail = False, url_path='logout',url_name='logout')
    def user_logout(self,request):
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'status': 'Logged out'})
        else:
            return HttpResponseForbidden()
    
    
    def get_permissions(self):
        '''permissions for different types of methods'''
        if self.request.method == 'GET':
            self.permission_classes = [IsEnabeled]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [IsAdmin,IsEnabeled]
        elif self.request.method == 'POST' or self.request.method == 'DELETE':
            self.permission_classes = [NobodyCan,IsEnabeled]

        return super(UserViewSet, self).get_permissions()
    
    def dispatch(self, *args, **kwargs):
        response = super(UserViewSet, self).dispatch(*args, **kwargs)
        response['Access-Control-Allow-Origin']='http://localhost:3000'
        response['Access-Control-Allow-Credentials']='true'

        return response

    
class CardsOfAUser(APIView):
    '''get projects for a particular user other than the request user'''
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsEnabeled]

    def get(self, request, pk ,format=None):
        user = Users.objects.get(id=pk)
        user_data = CardProjectSerializer(user.cards.all(), many = True)
        return Response(user_data.data)

class ProjectsOfAUser(APIView):
    '''get projects for a particular user other than the request user'''
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsEnabeled]

    def get(self, request, pk ,format=None):
        user = Users.objects.get(id=pk)
        user_data = ProjectCardSerializer(user.projects.all(), many = True)
        return Response(user_data.data)

class ProjectViewSet(viewsets.ModelViewSet):
    '''create/list/update/delete/retrieve project with needed permissions for each type of method'''
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def perform_create(self,serializer):
       serializer.save(creator = self.request.user)
    
    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsEnabeled]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
                self.permission_classes = [IsAdminOrProjectAdminOrCreator]

        return super(ProjectViewSet, self).get_permissions()
     
    def dispatch(self, *args, **kwargs):
        response = super(ProjectViewSet, self).dispatch(*args, **kwargs)
        response['Access-Control-Allow-Origin']='http://localhost:3000'
        response['Access-Control-Allow-Credentials']='true'

        return response

class ListViewSet(viewsets.ModelViewSet):
    '''create/list/update/delete/retrieve list with needed permissions for each type of method'''
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsEnabeled]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            self.permission_classes = [IsAdminOrTeamMember_l,IsEnabeled]
        elif self.request.method == 'POST':
            try:
                proj = Project.objects.get(id=int(self.request.data.get('project_l'))) 
                if(self.request.user in proj.members_p.all()):
                    self.permission_classes = [IsEnabeled]
                elif(self.request.user in proj.project_admins.all()):
                    self.permission_classes = [IsEnabeled]
                elif(self.request.user==proj.creator):
                    self.permission_classes = [IsEnabeled]
                else:
                    self.permission_classes = [NobodyCan]
            except:
                self.permission_classes = [IsAdminOrTeamMember_l,IsEnabeled]

        return super(ListViewSet, self).get_permissions()

class CardViewSet(viewsets.ModelViewSet):
    '''create/list/update/delete/retrieve card with needed permissions for each type of method'''
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsEnabeled]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            self.permission_classes = [IsAdminOrTeamMember_c,IsEnabeled]
        elif self.request.method == 'POST':
            try:
                proj = Project.objects.get(id=int(self.request.data.get('project_c'))) 
                list = List.objects.get(id=int(self.request.data.get('list_c')))
                print(proj)
                print(list)
                print(list.project_l)
                if(list.project_l!=proj):
                    self.permission_classes = [NobodyCan]
                elif(self.request.user in proj.members_p.all()):
                    self.permission_classes = [IsEnabeled]
                elif(self.request.user in proj.project_admins.all()):
                    self.permission_classes = [IsEnabeled]
                elif(self.request.user == proj.creator):
                    self.permission_classes = [IsEnabeled]
                # elif (self.request.user in list.members_l.all()):
                #     self.permission_classes = [IsEnabeled]
                else:
                    self.permission_classes = [NobodyCan]
            except:
                self.permission_classes = [IsAdminOrTeamMember_l,IsEnabeled]
        return super(CardViewSet, self).get_permissions()
  
class ListOfProjects(APIView):
    '''list all the lists of a given project'''
    permission_classes = [IsEnabeled]

    def get(self, request, pk ,format=None):
        proj = Project.objects.get(id=pk)
        serializer = ListProjectSerializer(proj.listsOfProject.all(), many = True)
        return Response(serializer.data)
   
class CardsOfLists(APIView):
    '''list all the cards of a given project'''
    permission_classes = [IsEnabeled]

    def get(self, request, pk ,format=None):
        list = List.objects.get(id=pk)
        serializer = CardProjectSerializer(list.cardsOfList.all(), many = True)
        return Response(serializer.data)

class CommentsOfACard(APIView):
    '''comments of a particular card'''
    permission_classes = [IsEnabeled]

    def get(self, request, pk ,format=None):
        card = Card.objects.get(id=pk)
        serializer = CommentCUserSerializer(card.commentsOfCard.all(), many = True)
        return Response(serializer.data)

class CommentPViewSet(viewsets.ModelViewSet):
    '''create/list/update/delete/retrieve comments on a particular project with needed permissions for each type of method'''
    queryset = Comment_p.objects.all()
    serializer_class = CommentPSerializer

    def perform_create(self,serializer):
        serializer.save( sender=self.request.user, time=datetime.now )

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsEnabeled]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [CommentEdit,IsEnabeled]
        elif self.request.method == 'DELETE' :
            self.permission_classes = [CommentPDelete,IsEnabeled]

        return super(CommentPViewSet, self).get_permissions()

class CommentCViewSet(viewsets.ModelViewSet):
    '''create/list/update/delete/retrieve comments on a particular project with needed permissions for each type of method'''
    queryset = Comment_c.objects.all()
    serializer_class = CommentCUserSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ser = CommentCSerializer(instance=instance)
        group_name = 'chat_card_'+ str(ser.data['card'])
        if instance.sender == request.user:
            self.perform_destroy(instance)
        else:
            return Response({"error": "comment can be modified only by its owner"}, status=status.HTTP_401_UNAUTHORIZED)
        async_to_sync(channel_layer.group_send)(group_name, {"type": "delete_comment", "message":ser.data})
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # print(instance)
        if(instance.sender==request.user):
            self.perform_update(serializer)
        else:
            return Response({"error":"comment can be modified only by its creator"}, status=status.status.HTTP_400_BAD_REQUEST)
        ser = CommentCUserSerializer(instance=instance)
        print(ser, ser.data)
        group_name = 'chat_card_'+ str(ser.data['card'])
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        async_to_sync(channel_layer.group_send)(group_name, {"type": "modify_comment", "message":ser.data})
        return Response(serializer.data)

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            self.permission_classes = [IsEnabeled]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            self.permission_classes = [CommentEdit,IsEnabeled]
        elif self.request.method == 'DELETE' :
            self.permission_classes = [CommentCDelete,IsEnabeled]

        return super(CommentCViewSet, self).get_permissions()



'''login through oauth'''
def oauth_redirect(req):
    url = f"https://channeli.in/oauth/authorise/?client_id={auth_pa['CLIENT_ID']}&redirect_uri={auth_pa['REDIRECT_URI']}&state={auth_pa['STATE_STRING']}"
    return HttpResponseRedirect(url)

class Login2(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    @action(methods=['GET'], detail = False)
    def login2(self,req):
        user = Users.objects.get(id=1)
        login(req,user)
        return HttpResponse('Hii')

class Login_oauth(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self,req):
        try:
            auth_code = self.request.query_params.get('code')
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
                if(student.banned):
                    return HttpResponse("U are banned")
            except models.Users.DoesNotExist:
                student = models.Users(
                    username = data_stu['username'],
                    name = data_stu['person']['fullName'],
                    is_admin = False,
                    details = 'Maintainer',
                    banned = False
                )
                student.save()
            try:
                login(request=req, user=student)
            except:
                print("kya kare nahi hora")
            res= Response( status=status.HTTP_202_ACCEPTED)
            res['Access-Control-Allow-Origin']='http://localhost:3000'
            res['Access-Control-Allow-Credentials']='true'
            return res
        else : 
            HttpResponse("This app can only be accessed by IMG members :p")
        return HttpResponse("hi")   


    