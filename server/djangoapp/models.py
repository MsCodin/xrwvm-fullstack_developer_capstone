from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CarMake(models.Model):
    """Model representing a car manufacturer/make."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Model representing a specific car model linked to a CarMake."""
    CAR_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
        ('Hatchback', 'Hatchback'),
        ('Coupe', 'Coupe'),
        ('Truck', 'Truck'),
    ]
    car_make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name='car_models'
    )
    dealer_id = models.IntegerField(
        help_text="ID of the dealer in Cloudant/MongoDB"
    )
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=50,
        choices=CAR_TYPE_CHOICES,
        default='Sedan'
    )
    year = models.IntegerField(
        validators=[
            MinValueValidator(2015),
            MaxValueValidator(2023)
        ]
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
