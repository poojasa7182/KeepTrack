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

urlpatterns = [
    path('login', oauth_redirect, name="oauth_redirect"),
    path('',include(router.urls)),
    path('list/<int:pk>/cards', ListOfProjects.as_view()),
    path('project/<int:pk>/list', CardsOfLists.as_view()),
    path('user/<int:pk>/tasks', ProjectsOfAUser.as_view()),
    path('betw',oauth_fetch_data,name="oauth_fetch_data")
]
