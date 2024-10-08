from django.db import models

# Create your models here.
class PLANS(models.Model):
    name = models.CharField(max_length= 200)
    img = models.ImageField(upload_to= 'pics')
    price = models.IntegerField()
    options = models.BooleanField(default=False)