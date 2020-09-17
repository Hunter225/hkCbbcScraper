from rest_framework import serializers
from .models import BullBearRatioSchema, StockSchema
import json

class CbbcSerializer(serializers.ModelSerializer):

    stock_abbv = serializers.CharField(source='stock.stock_abbv', required=False, allow_null=True)
    cbbc_abbv = serializers.CharField(source='stock.cbbc_abbv', required=False, allow_null=True)
    is_index = serializers.CharField(source='stock.is_index', required=False, allow_null=True)

    class Meta:
        model = BullBearRatioSchema
        fields = ['trade_date', 
                    'bull_hedge_volume',
                    'bear_hedge_volume',
                    'bull_chips_amount',
                    'bear_chips_amount',
                    'bull_bear_ratio_for_chips',
                    'bull_bear_ratio_for_hedge_volume',
                    'bull_weighted_average',
                    'bear_weighted_average',
                    'close_price',
                    'stock_abbv',
                    'cbbc_abbv',
                    'is_index']