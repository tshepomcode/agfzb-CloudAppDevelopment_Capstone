from http.client import HTTPResponse
from multiprocessing import context
import re
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_request, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context ={}
    # Handles POST request
    if request.method == 'POST':
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provided credentials can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)
    

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to the dealership reviews
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://f87164fc.eu-gb.apigw.appdomain.cloud/api/dealership"
        # url = "https://f87164fc.eu-gb.apigw.appdomain.cloud/api/dealership?state=Minnesota"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Add dealerships to context
        context["dealerships"] = dealerships
        print(context)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://f87164fc.eu-gb.apigw.appdomain.cloud/api/review"
        dealerships_reviews = get_dealer_by_id_from_cf(url, dealerId=dealer_id)
        # print(f'========> dealership reviews {dealerships_reviews}')
        # for review in dealerships_reviews:
        #     print(f"Review Details: Dealership {review.dealership} | Name: {review.name} \nReview: {review.review}")
        # Concat all dealer's short name
        context['reviews'] = dealerships_reviews
        context['dealer_id'] =  dealer_id
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships_reviews])
        return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    url = "https://f87164fc.eu-gb.apigw.appdomain.cloud/api/review"
    dealership = get_dealer_by_id_from_cf(url, dealerId=dealer_id)
    context["dealer"] = dealership

    if request.method == "GET":
        # Get cars models for the dealer
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        print(f"cars = CarModel.objects.filter(dealer_id=dealer_id)\n{cars}")
        context["cars"] =  cars
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        if request.user.is_authenticated:
            username = request.user.username
            print(f"request.POST:\n {request.POST}")
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["name"] = username
            payload["dealeship"] = dealer_id
            payload["time"] = datetime.utcnow().isoformat()
            payload["id"] = dealer_id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase-date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))

            json_payload = {}
            json_payload["review"] = payload
            
            review_post_url = "https://f87164fc.eu-gb.apigw.appdomain.cloud/api/review"
            response = post_request(review_post_url, json_payload, dealerId=dealer_id)
            print(response)

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            print("User is unauthenticated!")

