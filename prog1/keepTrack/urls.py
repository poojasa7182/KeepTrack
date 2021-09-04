"""urls"""
from django.urls import path,include
from keepTrack import views
from .views import *
from rest_framework.routers import DefaultRouter


app_name = 'keepTrack'

router = DefaultRouter()

router.register(r'user',views.UserViewSet, basename='user')
router.register(r'project',views.ProjectViewSet, basename='project')

urlpatterns = [
    path('login', oauth_redirect, name="oauth_redirect"),
    path('',include(router.urls)),
    # path('/ok',complete,name="after_oauth"),
    path('betw',oauth_fetch_data,name="oauth_fetch_data")
]
