from django.db import models



class Holidays(models.Model):
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=100)
    date = models.DateTimeField('date of holiday anviv')
    class Meta:
    	ordering = ['country_code','date']
    def __str__(self):
        return self.name +" ON ==> " + str(self.date)