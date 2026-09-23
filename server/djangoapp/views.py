from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        else:
            return JsonResponse({"userName": username, "status": "Failed"}, status=401)
    except Exception as e:
        logger.error(f"Login error: {e}")
        return JsonResponse({"error": "Invalid request"}, status=400)


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    try:
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"}, status=409)
        
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return JsonResponse({"error": "Invalid request"}, status=400)


# === Car Data Functions ===
def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]
    
    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(
            CarMake.objects.create(name=data['name'], description=data['description'])
        )

    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023, "dealer_id": 1, "car_make": car_make_instances[0]},
        {"name": "Qashqai", "type": "SUV", "year": 2023, "dealer_id": 1, "car_make": car_make_instances[0]},
        {"name": "XTRAIL", "type": "SUV", "year": 2023, "dealer_id": 1, "car_make": car_make_instances[0]},
        {"name": "A-Class", "type": "SUV", "year": 2023, "dealer_id": 2, "car_make": car_make_instances[1]},
        {"name": "C-Class", "type": "SUV", "year": 2023, "dealer_id": 2, "car_make": car_make_instances[1]},
        {"name": "E-Class", "type": "SUV", "year": 2023, "dealer_id": 2, "car_make": car_make_instances[1]},
        {"name": "A4", "type": "SUV", "year": 2023, "dealer_id": 3, "car_make": car_make_instances[2]},
        {"name": "A5", "type": "SUV", "year": 2023, "dealer_id": 3, "car_make": car_make_instances[2]},
        {"name": "A6", "type": "SUV", "year": 2023, "dealer_id": 3, "car_make": car_make_instances[2]},
        {"name": "Sorrento", "type": "SUV", "year": 2023, "dealer_id": 4, "car_make": car_make_instances[3]},
        {"name": "Carnival", "type": "SUV", "year": 2023, "dealer_id": 4, "car_make": car_make_instances[3]},
        {"name": "Cerato", "type": "Sedan", "year": 2023, "dealer_id": 4, "car_make": car_make_instances[3]},
        {"name": "Corolla", "type": "Sedan", "year": 2023, "dealer_id": 5, "car_make": car_make_instances[4]},
        {"name": "Camry", "type": "Sedan", "year": 2023, "dealer_id": 5, "car_make": car_make_instances[4]},
        {"name": "Kluger", "type": "SUV", "year": 2023, "dealer_id": 5, "car_make": car_make_instances[4]},
    ]
    
    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            car_make=data['car_make'],
            type=data['type'],
            year=data['year'],
            dealer_id=data['dealer_id']
        )


def get_cars(request):
    """Return all car makes with their models as JSON"""
    makes = CarMake.objects.all()
    data = []
    for make in makes:
        models = CarModel.objects.filter(car_make=make)
        data.append({
            "name": make.name,
            "description": make.description,
            "models": [
                {"name": m.name, "type": m.type, "year": m.year, "dealer_id": m.dealer_id}
                for m in models
            ]
        })
    return JsonResponse({"cars": data})


# === Dealership & Review Functions ===
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})


def get_dealer_reviews(request, dealer_id):
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)
    
    if reviews:
        for review_detail in reviews:
            sentiment = analyze_review_sentiments(review_detail['review'])
            if sentiment:
                review_detail['sentiment'] = sentiment.get('sentiment', 'neutral')
            else:
                review_detail['sentiment'] = 'neutral'
    
    return JsonResponse({"status": 200, "reviews": reviews})
