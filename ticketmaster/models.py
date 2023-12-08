from django.db import models


# Create your models here.

# Adrian: Created database for search inputs (for testing purposes) and for the CRUD operation, will implement later.
class SearchInput(models.Model):
    search = models.CharField(max_length=200)
    location = models.CharField(max_length=200)


# Adrian: Created database which stores information of an event
class EventTable(models.Model):
    eventImage = models.CharField(max_length=400, default="N/A")
    eventName = models.CharField(max_length=200)
    eventLocation = models.CharField(max_length=200)
    eventDate = models.CharField(max_length=200, default="N/A")
    eventTime = models.CharField(max_length=200, default="N/A")
    eventTicketURL = models.CharField(max_length=300)
    favorite = models.BooleanField(default=False)


