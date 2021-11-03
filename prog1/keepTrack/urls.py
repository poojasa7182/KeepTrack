"""urls"""
from django.urls import path,include
from keepTrack import views
from .views import *
from rest_framework.routers import DefaultRouter


app_name = 'keepTrack'

router = DefaultRouter()

router.register(r'user',views.UserViewSet, basename='user')
router.register(r'project',views.ProjectViewSet, basename='project')
router.register(r'list',views.ListViewSet, basename='list')
router.register(r'card',views.CardViewSet, basename='card')
router.register(r'comments_c',views.CommentCViewSet, basename='comment_c')
router.register(r'comments_p',views.CommentPViewSet, basename='comment_p')
router.register(r'login2',views.Login2, basename='login2')

urlpatterns = [
    path('login', oauth_redirect, name="oauth_redirect"),
    path('',include(router.urls)),
    path('list/<int:pk>/cards', CardsOfLists.as_view()),
    path('project/<int:pk>/list', ListOfProjects.as_view()),
    path('users/<int:pk>/tasks', CardsOfAUser.as_view()), 
    path('users/<int:pk>/projects', ProjectsOfAUser.as_view()),
    path('card/<int:pk>/comments', CommentsOfACard.as_view()),
    path('betw',Login_oauth.as_view())
]
