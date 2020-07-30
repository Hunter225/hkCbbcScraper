import csv
import pandas as pd
from datetime import datetime
from hkCbbcApi.models import StockSchema, BullBearRatioSchema
import glob


def run():
    data_csv_filenames = glob.glob('hkex_cbbc_data/*.csv')
    for filename in data_csv_filenames:
        cbbc_data = pd.read_csv(filename, sep='"\t"', encoding="utf-16", 
                                header=0, usecols=['CBBC Name' ,'Trade Date', 'Underlying', 'Bull/Bear', 'No. of CBBC still out in market *', 'Closing Price', 'Ent. Ratio^'])
        trade_dates = [trade_date for trade_date in cbbc_data['Trade Date'].unique() if trade_date != None]
        underlying_assets = [underlying_asset for underlying_asset in cbbc_data['Underlying'].unique() if underlying_asset != None]

        for trade_date in trade_dates:
            for underlying_asset in underlying_assets:

                # Bull part
                cbbc_datum = cbbc_data[(cbbc_data['Bull/Bear'] == 'Bull      ') & \
                                        (cbbc_data['Underlying'] == underlying_asset) & \
                                        (cbbc_data['Trade Date'] == trade_date)]
                if underlying_asset == 'HSI' or 'HSCEI':
                    cbbc_datum['hedging_volume'] = cbbc_datum['No. of CBBC still out in market *'] / cbbc_datum['Ent. Ratio^'] / 50
                else:
                    cbbc_datum['hedging_volume'] = cbbc_datum['No. of CBBC still out in market *'] / cbbc_datum['Ent. Ratio^']

                cbbc_datum['chips_amount'] = cbbc_datum['Closing Price'] * cbbc_datum['No. of CBBC still out in market *']
                
                bull_hedge_volume = cbbc_datum['hedging_volume'].sum()
                bull_chips_amount = cbbc_datum['chips_amount'].sum()


                # Bear part
                cbbc_datum = cbbc_data[(cbbc_data['Bull/Bear'] == 'Bear      ') & \
                                        (cbbc_data['Underlying'] == underlying_asset) & \
                                        (cbbc_data['Trade Date'] == trade_date)]
                if underlying_asset == 'HSI' or 'HSCEI':
                    cbbc_datum['hedging_volume'] = cbbc_datum['No. of CBBC still out in market *'] / cbbc_datum['Ent. Ratio^'] / 50
                else:
                    cbbc_datum['hedging_volume'] = cbbc_datum['No. of CBBC still out in market *'] / cbbc_datum['Ent. Ratio^']

                cbbc_datum['chips_amount'] = cbbc_datum['Closing Price'] * cbbc_datum['No. of CBBC still out in market *']
                
                bear_hedge_volume = cbbc_datum['hedging_volume'].sum()
                bear_chips_amount = cbbc_datum['chips_amount'].sum()

                # meta data
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
                scrape_date = datetime.now()
                stock_abbv = underlying_asset.lstrip("0")
                cbbc_abbv = cbbc_datum['CBBC Name'].iloc[0][3:8].rstrip()
                stock_obj, created = StockSchema.objects.get_or_create(stock_abbv=stock_abbv, defaults=dict(status='A', is_index=False, cbbc_abbv=cbbc_abbv))
                stock_id = stock_obj.id

                # bull bear ratio calculation
                bull_bear_ratio_for_hedge_volume = bull_hedge_volume / bear_hedge_volume
                bull_bear_ratio_for_chips = bull_chips_amount / bear_chips_amount

                bull_bear_data = dict(status='A', scrape_datetime=scrape_date, bull_hedge_volume=bull_hedge_volume,
                                        bear_hedge_volume=bear_hedge_volume, bull_bear_ratio_for_hedge_volume=bull_bear_ratio_for_hedge_volume,
                                        bull_chips_amount=bull_chips_amount, bear_chips_amount=bear_chips_amount,
                                        bull_bear_ratio_for_chips=bull_bear_ratio_for_chips)

                BullBearRatioSchema.objects.update_or_create(stock_id=stock_obj, trade_date=trade_date_obj, defaults=bull_bear_data)