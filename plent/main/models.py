from django.db import models
from django.conf import settings

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user}"
    
class Post(models.Model):
    topic = models.CharField(max_length=256)
    content = models.TextField()
    authors = models.ManyToManyField(Client)
    
    def __str__(self):
        return f"{self.topic}"