from django.db import models
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('stars'))
        return avg if avg else 0
    


    
STARS = (
    (i, i) for i in range(1, 6)
)

class Review(models.Model):
    text = models.TextField(max_length=300)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='reviews')
    stars = models.IntegerField(choices=STARS, default=5)

    def __str__(self):
        return self.text
    


    
    

    