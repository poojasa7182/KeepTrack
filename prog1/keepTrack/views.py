from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from requests.api import request
from django.contrib.auth import login
from .CONFIG import auth_pa
from . import models
from rest_framework.decorators import action
import json
import requests
# Create your views here.

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