from django.db import models


# Create your models here.
class StockQuote(models.Model):
    stock_ticker = models.CharField(max_length=200)
    access_date = models.DateTimeField('date accessed')

    def __str__(self):
        return self.stock_ticker
