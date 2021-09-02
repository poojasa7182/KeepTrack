"""urls"""
from django.urls import path
from .views import *

app_name = 'keepTrack'
urlpatterns = [
    path('login', oauth_redirect, name="oauth_redirect"),
    # path('/ok',complete,name="after_oauth"),
    path('betw',oauth_fetch_data,name="oauth_fetch_data")
]
