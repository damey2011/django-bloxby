from django.db import models


# Create your models here.
class Application(models.Model):
    name = models.CharField(max_length=50)
    auth_url = models.URLField(max_length=500, help_text='URL that authenticated uploader')
    receiving_url = models.URLField(max_length=500, help_text='URL that receives the file')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
