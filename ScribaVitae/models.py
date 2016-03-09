from django.conf import settings
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class LiteraryWork(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE )
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    dateAdded = models.DateTimeField('date published')
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(max_length=10000)
    literaryWork = models.ForeignKey(LiteraryWork,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    dateAdded = models.DateTimeField('date published')
    def __str__(self):
        return self.content