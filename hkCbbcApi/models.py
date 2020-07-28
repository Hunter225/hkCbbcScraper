from django.db import models
import constants

# Create your models here.

class StockSchema(models.Model):
    class Meta:
        ordering = ('created_on',)
        db_table = 'stocks'

    #standard settings
    status_values = {constants.status_active: 'A', constants.status_deleted: 'D'}
    created_on = models.DateTimeField(null=False, auto_now_add=True)
    modified_on = models.DateTimeField(null=False, auto_now=True)
    status = models.CharField(null=False, max_length=3, default='I')

    def get_status(self):
        if  self.status == 'A':
            return constants.status_active
        elif  self.status == 'D':
            return constants.status_deleted

    #fields
    stock_abbv = models.CharField(null=True, max_length=255, blank=False)
    stock_name = models.CharField(null=True, max_length=255, blank=False)



class BullBearRatioSchema(models.Model):
    class Meta:
        ordering = ('created_on',)
        db_table = 'bull_bear_ratios'
        
    #standard settings
    status_values = {constants.status_active: 'A', constants.status_deleted: 'D'}
    created_on = models.DateTimeField(null=False, auto_now_add=True)
    modified_on = models.DateTimeField(null=False, auto_now=True)
    status = models.CharField(null=False, max_length=3, default='I')
    
    def get_status(self):
        if  self.status == 'A':
            return constants.status_active
        elif  self.status == 'D':
            return constants.status_deleted

    # fields
    trade_date = models.DateField(null=True, blank=False)
    scrape_datetime = models.DateTimeField(null=True, blank=False)
    bull_volume = models.IntegerField(null=True, blank=False)
    bear_volume = models.IntegerField(null=True, blank=False)
    close_price = models.FloatField(null=True, blank=False)
    bull_amount = models.FloatField(null=True, blank=False)
    bear_amount = models.FloatField(null=True, blank=False)
    bull_bear_ratio = models.FloatField(null=True, blank=False)

    # Foreign key
    stock = models.ForeignKey(StockSchema, on_delete=models.PROTECT, null=True, related_name='bull_bear_ratio')
