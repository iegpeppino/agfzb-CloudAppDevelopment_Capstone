from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer, CarModel, CarMake
# from .restapis import related methods
from .restapis import get_dealer_reviews_from_cf, get_dealers_from_cf , post_request, get_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about_us.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact_us.html', context)
# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username = username , password = password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password." 
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)        

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
# Check for existing users
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username = username)
            user_exist = True
        except:
            logger.error("New User")
        if not user_exist:
            user = User.objects.create_user(username = username, password = password,
                                             first_name = first_name, last_name = last_name)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'This user already exists, try a different username.' 
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://9e850b66.us-south.apigw.appdomain.cloud/api/dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {}
        context['dealerships'] = dealerships
        # Return a list of dealer short names
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://9e850b66.us-south.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id = dealer_id)
        context['reviews'] = reviews
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request, dealer_id):
    context = {}
    user = request.user
    # GET request to access the available dealerships and cars to review
    if request.method == "GET":
        cars = CarModel.objects.filter(dealer_id= dealer_id)
        context["cars"] = cars
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        # If the user is authenticated it will let him post a review
        if user.is_authenticated:
            url = "https://9e850b66.us-south.apigw.appdomain.cloud/api/review"
            review = {}
            review["dealership"] = dealer_id
            review["name"] = user.first_name +' '+ user.last_name
            review["review"] = request.POST["review_body"]
            review["purchase"] = request.POST.get("purchasecheck") == "on"
            # Data that is only available if a car was purchased
            thedealer = get_dealers_from_cf("https://9e850b66.us-south.apigw.appdomain.cloud/api/dealerships")
            context["thedealer"] = thedealer
            if request.POST.get("purchasecheck") == "on":
                review["purchase_date"] = request.POST["purchase_date"]
                car = CarModel.objects.get(pk= request.POST["car"])
                review["car_make"] = car.carmake.name
                review["car_model"] = car.name
                # Convert the value date for years to string 
                review["car_year"] = car.year.strftime("%Y")
            json_payload = {}
            json_payload["review"] = review
            print(json_payload)
            result = post_request(url, json_payload, dealer_id= dealer_id)
            print("POST result: ")
            print(result)
            context["dealer_id"] = dealer_id
            return redirect("/djangoapp/dealer/" + str(dealer_id),context)