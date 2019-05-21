from django.shortcuts import render, get_object_or_404, render_to_response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib import auth
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
import datetime
from django.core import serializers #Convert to JSON
from .serializers import *
from django.core.cache import cache
from django_redis import get_redis_connection
import pickle

r = get_redis_connection("default")  #for raw_redis


def index(request):
    # r.delete('userlogdict')
    return render(request, 'index.html')

@csrf_exempt
@api_view(["POST"])
def userlogin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        user = request.user  #Request current user
        user = user.id  #Request USER ID
        now = datetime.datetime.now().replace(microsecond=0)  
        message = str(now) + " LoginAPI Triggered**" + str(user)
        #Check if cache persists
        if r.get('userlogdict') == None:
            SetCacheUser(user, message)
            print("created")
        else:
            print("Existing found")
            GetDict = r.get('userlogdict')
            userlog = pickle.loads(GetDict)
            userlog["log"] += "|log|" + message
            print(userlog)
            pickle_userlog = pickle.dumps(userlog) #Using Pickle
            r.set('userlogdict', pickle_userlog)
        return Response("Logged in", status=HTTP_200_OK)
    else:
        return Response("Invalid Credentials", status = HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
def userlogout(request):
    user = request.user  #New
    user = user.id  #New
    now = datetime.datetime.now().replace(microsecond=0)  #New
    message = str(now) + " LogoutAPI Triggered**" + str(user)
    #Check if cache persists
    if r.get('userlogdict') == None:
        SetCacheUser(user, message)
        print("created")
    else:
        print("Existing cache found")
        GetDict = r.get('userlogdict')
        userlog = pickle.loads(GetDict)
        userlog["log"] += "|log|" + message
        print(userlog)
        pickle_userlog = pickle.dumps(userlog) #Using Pickle
        r.set('userlogdict', pickle_userlog)
    # 
    auth.logout(request)
    return Response("LoggedOut")

@csrf_exempt
@api_view(["POST"])
def activate(request):
    user = request.user
    user = user.id
    now = datetime.datetime.now().replace(microsecond=0)  #New
    message = str(now) + " ActivateAPI Triggered**" + str(user)
    #Check if cache persists
    if r.get('userlogdict') == None:
        SetCacheUser(user, message)
        print("created")
    else:
        print("Existing cache found")
        # r.delete('userlogdict')
        # UserLogger()
        GetDict = r.get('userlogdict')
        userlog = pickle.loads(GetDict)
        userlog["log"] += "|log|" + message
        print(userlog)
        pickle_userlog = pickle.dumps(userlog) #Using Pickle
        r.set('userlogdict', pickle_userlog)
    # 
    return Response(message)

@csrf_exempt
@api_view(["POST"])
def ring(request):
    user = request.user
    user = user.id
    now = datetime.datetime.now().replace(microsecond=0)  #New
    message = str(now) + " RingAPI Triggered**" + str(user)
    #Check if cache persists
    if r.get('userlogdict') == None:
        SetCacheUser(user, message)
        print("created")
    else:
        print("Existing Cache found")
        # print(r.ttl('userlogdict'))
        GetDict = r.get('userlogdict')
        userlog = pickle.loads(GetDict)
        userlog["log"] += "|log|" + message
        print("Cache")
        print(userlog)
        pickle_userlog = pickle.dumps(userlog) #Using Pickle
        r.set('userlogdict', pickle_userlog)
    # 
    return Response(message)
    


# User function
def SetCacheUser(user, message):
    print("Setting up cache")
    userlog = {"log": message}
    print("Cache")
    print(userlog)
    pickle_userlog = pickle.dumps(userlog) #Using Pickle
    r.set('userlogdict', pickle_userlog)
    return 1

# Cron functions
def UserLogger():
    print("Executing Function")
    if r.get('userlogdict') != None:
        print("Executing IF")
        GetDict = r.get('userlogdict')
        userlog = pickle.loads(GetDict)
        # Get individual logs
        logs = userlog['log'].split("|log|")
        print(logs)
        for eachlog in logs:
            xuser = eachlog.split("**")
            print(xuser[0])
            data = {
                'log': xuser[0],
                'user': int(xuser[1])
            }

            serializer = LoggerSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                print("Completed")
            else:
                print("Not Found")
        r.delete('userlogdict')

