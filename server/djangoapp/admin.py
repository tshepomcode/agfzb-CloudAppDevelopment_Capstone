from django.contrib import admin

# from server.djangoapp.models import CarMake, CarModel
from .models import CarMake, CarModel


# Register your models here.


# CarModelInline class
class CarModelInline(admin.StackedInline):
  model = CarModel
  extra = 3

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
  fields = ['name', 'dealerid', 'car_type', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
  fields = ['name', 'description']
  inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
