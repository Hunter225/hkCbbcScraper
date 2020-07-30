from django.db import models
import constants, enums

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
    stock_name_en = models.CharField(null=True, max_length=255, blank=False)
    stock_name_zh = models.CharField(null=True, max_length=255, blank=False)
    cbbc_abbv = models.CharField(null=True, max_length=255, blank=False)
    is_index = models.BooleanField(default=False)



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
    bull_hedge_volume = models.FloatField(null=True, blank=False)
    bear_hedge_volume = models.FloatField(null=True, blank=False)
    bull_chips_amount = models.FloatField(null=True, blank=False)
    bear_chips_amount = models.FloatField(null=True, blank=False)
    bull_bear_ratio_for_chips = models.FloatField(null=True, blank=False)
    bull_bear_ratio_for_hedge_volume = models.FloatField(null=True, blank=False)
    source = models.IntegerField(null=False, default=enums.CbbcDataSourceEnum.hkex.value, choices=[(tag, tag.value) for tag in enums.CbbcDataSourceEnum])
    close_price = models.FloatField(null=True, blank=False)

    # Foreign key
    stock = models.ForeignKey(StockSchema, on_delete=models.PROTECT, null=True, related_name='bull_bear_ratio')
