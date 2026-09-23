# Uncomment the required imports before adding the code
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
# from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create a `login_user` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    
    # Try to authenticate
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    
    if user is not None:
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}
    
    return JsonResponse(response_data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print(f"Log out the user `{request.user.username}`")
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    if request.method == 'GET':
        return JsonResponse({"message": "Send POST data to register"})
    elif request.method == 'POST':
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        email = data.get('email', '')
        
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except User.DoesNotExist:
            logger.debug(f"{username} is new user")
        
        if not user_exist:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Registered"})
        else:
            return JsonResponse({"error": "User already exists"})
