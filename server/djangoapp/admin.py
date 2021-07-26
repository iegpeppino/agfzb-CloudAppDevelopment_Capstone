from django.contrib import admin
from .models import  CarMake, CarModel
# from .models import related models


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3
# CarModelAdmin class

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    fields = ('name', 'description', 'country')

# Register models here
admin.site.register(CarModel)
admin.site.register(CarMake, CarMakeAdmin)
