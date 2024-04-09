from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework import serializers

# Create your models here.
class User(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    residence = models.CharField(max_length=150, blank=True, null=True)
    
class Skill(models.Model):
    class Language(models.TextChoices):
        CPP = "C++"
        JAVASCRIPT = "Javascript"
        PYTHON = "Python"
        JAVA = "Java"
        LUA = "Lua"
        RUST = "Rust"
        GO = "Go"
        JULIA = "Julia"

    class Level(models.TextChoices):
        BEGINNER = "beginner"
        EXPERIENCED = "experienced"
        EXPERT = "expert"

    level = models.CharField(max_length=50, choices=Level.choices)
    language = models.CharField(max_length=50, choices=Language.choices)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Project(models.Model):
    project_name = models.CharField(max_length=150)
    description = models.TextField()
    maximum_collaborators = models.IntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner", default="null")
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="collaborators", blank=True)
    complete = models.BooleanField(default=False)

        # def save(self, *args, **kwargs):
    #     self.open_seats = self.maximum_collaborators - self.collaborators.count()
    #     return super().save(*args, **kwargs)


class CollaborationRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="request_project")
    status = models.CharField(max_length=10, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("declined", "Declined")])

