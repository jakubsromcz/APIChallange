from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)
    countryCode = models.CharField(max_length=2)
    createdAt = models.DateTimeField(auto_now_add=True)
    groupId = models.IntegerField(null=True)  # Allow null for initial creation

    def __str__(self):
        return self.name
