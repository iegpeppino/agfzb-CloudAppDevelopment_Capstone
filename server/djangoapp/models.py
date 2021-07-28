from django.db import models
from django.utils.timezone import now
from django_countries.fields import CountryField

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null = False, max_length = 20)
    description = models.TextField(max_length=300)
    country = CountryField()

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description + "," + \
                "Country:" + self.country

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to proitide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    name = models.CharField(null= False, max_length= 20)
    year = models.DateField()
    dealer_id = models.IntegerField()
    TYPE_CHOICES = [
        ("sedan" , "Sedan"),
        ("suv" , "SUV"),
        ("wagon" , "Wagon"),
        ("hatchback" , "Hatchback"),
        ("pickup" , "Pickup"),
        ]
    type = models.CharField(
        max_length= 20,
        choices= TYPE_CHOICES,
        default= 'sedan'
    )
    isused = models.BooleanField(default= False)
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Year: " + str(self.year) + "," + \
               "Type: " + self.type + "," + \
                "Is used : Yes" if self.isused else "Is used : No"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        self.id = id
        self.full_name = full_name
        self.short_name = short_name
        self.state = state
        self.st = st
        self.city = city
        self.address = address
        self.zip = zip
        self.lat = lat
        self.long = long
    def __str__(self):
        "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data

class DealerReview:
    def __init__(self, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
    def __str__(self):
        "Reviewer : " + self.name 