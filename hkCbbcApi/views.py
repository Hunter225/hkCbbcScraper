from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CbbcSerializer
from .models import StockSchema, BullBearRatioSchema
from datetime import datetime, timedelta


class CbbcViewSet(APIView):

    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('stock_code')
        start_date = datetime.strptime(request.query_params.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.query_params.get('end_date'), '%Y-%m-%d')
        if (end_date - start_date) > timedelta(days=30):
            return Response({'msg': 'query too much data'})
        stock_id = StockSchema.objects.get(stock_abbv = stock_code)
        cbbc_qs = BullBearRatioSchema.objects.filter(stock_id=stock_id, trade_date__range=[start_date, end_date]).order_by('trade_date')

        serialized = CbbcSerializer(cbbc_qs, many=True)
        return Response(serialized.data)