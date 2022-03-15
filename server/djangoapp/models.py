from tkinter import CASCADE
from django.db import models
from django.forms import DateField
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=255)

  def __str__(self) -> str:
      return f'Name {self.name} \nDescription{self.description}'


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
  SEDAN = 'sedan'
  SUV = 'SUV'
  WAGON = 'WAGON'
  COUPE = 'COUPE'
  CAR_TYPE_CHOICES = [
    (SEDAN, 'Sedan'),
    (SUV, 'SUV'),
    (WAGON, 'Wagon'),
    (COUPE, 'Coupe')
  ]
  car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  dealer_id = models.IntegerField()
  car_type = models.CharField(
    max_length=10,
    choices=CAR_TYPE_CHOICES,
    default=SEDAN
  )
  year = models.DateField()


  def __str__(self) -> str:
      return f'Name: {self.name} Dealer ID: {self.dealer_id} Car Type: {self.car_type}' \
        + f'Year: {self.year}'


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
      # Dealer address
      self.address = address
      # Dealer city
      self.city = city
      # Dealer Full Name
      self.full_name = full_name
      # Dealer id
      self.id = id
      # Location lat
      self.lat = lat
      # Location long
      self.long = long
      # Dealer short name
      self.short_name = short_name
      # Dealer state short
      self.st = st
      # Dealer state
      self.state = state
      # Dealer zip
      self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
