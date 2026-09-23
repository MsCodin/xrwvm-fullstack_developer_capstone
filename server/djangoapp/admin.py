from django.contrib import admin
from .models import CarMake, CarModel


# Inline class to display CarModel entries inside CarMake admin
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Show 1 empty form for adding new models by default


# Custom admin configuration for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'dealer_id')
    list_filter = ('car_make', 'type', 'year')
    search_fields = ('name', 'car_make__name')


# Custom admin configuration for CarMake with CarModel inline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'country', 'founded_year')
    search_fields = ('name',)
    inlines = [CarModelInline]  # Embed CarModel forms inside CarMake page


# Register models with their custom admin classes
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
