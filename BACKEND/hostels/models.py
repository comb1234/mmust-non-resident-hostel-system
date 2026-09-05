from django.db import models

class Hostel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    distance = models.CharField(max_length=50)
    price_per_semester = models.DecimalField(max_digits=10, decimal_places=2)
    rooms_available = models.IntegerField(default=0)
    total_rooms = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=[('Male','Male'), ('Female','Female'), ('Mixed','Mixed')])
    amenities = models.JSONField(default=list, blank=True)
    images = models.JSONField(default=list, blank=True, help_text="List of image paths (e.g., ['../assets/images/lurambi.jpg', ...])")
    rating = models.FloatField(default=0.0)
    contact = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name