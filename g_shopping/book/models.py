from django.db import models

# Create your models here.


class Chapter(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Concept(models.Model):
    name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, related_name='concept', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
