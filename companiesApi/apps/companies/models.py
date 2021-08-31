from django.db import models

# Create your models here.
class Companies(models.Model):
    name = models.CharField("Name", max_length=100,unique=True)
    website = models.URLField('WebSite', max_length=200)
    fundations = models.IntegerField()    

    
    def __str__(self):
        return self.name
