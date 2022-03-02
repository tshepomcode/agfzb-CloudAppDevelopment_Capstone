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
  name = models.CharField(max_length=30)
  description = models.CharField(max_length=255)

  def __str__(self) -> str:

      return f'CarMake({self.name},{self.description})'

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Models):
  SUV = 'SUV'
  SEDAN = 'SDN'
  WAGON = 'WGN'
  COUPE = 'CPE'
  HATCHBACK = 'HTB'
  MINIVAN = 'MVN'
  CONVERTIBLE = 'CNE'
  CAR_TYPE_CHOICES = [
    ('SUV', 'SMALL UTILITY VEHICLE'),
    ('SDN', 'Sedan'),
    ('WGN', 'Station Wagon'),
    ('CPE', 'Coupe'),
    ('HTB', 'Hatchback'),
    ('MVN', 'Minivan'),
    ('CNE', 'Convertible'),
  ]
  car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
  name = models.CharField(max_length=30)
  dealer_id = models.IntegerField()
  car_type = models.CharField(
    max_length=3,
    choices=CAR_TYPE_CHOICES,
    default=SEDAN
  )
  year = DateField('date made')

  def __str__(self) -> str:
      return f'CarMake({self.car_make}, {self.name}, {self.dealer_id}, {self.car_type}, {self.year})'




# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
