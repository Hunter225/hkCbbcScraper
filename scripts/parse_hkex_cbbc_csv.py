import csv
import pandas as pd
import os
from datetime import datetime, timedelta
from hkCbbcApi.models import StockSchema, BullBearRatioSchema
import glob
from yahoofinancials import YahooFinancials

def get_close_price(trade_date, underlying_asset):
    if underlying_asset == 'HSI':
        underlying_asset = '^HSI'
    elif underlying_asset == 'HSCEI':
        underlying_asset = '^HSCE'
    else:
        underlying_asset = underlying_asset[1:len(underlying_asset)] + '.HK'

    next_two_date = (datetime.strptime(trade_date, "%Y-%m-%d") + timedelta(days = 2)).strftime("%Y-%m-%d")
    yahoo_financials = YahooFinancials(underlying_asset)
    data = yahoo_financials.get_historical_price_data(trade_date, next_two_date, "daily")
    close_price = data[underlying_asset]['prices'][0]['close']

    return close_price

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
                bull_datum = cbbc_data[(cbbc_data['Bull/Bear'] == 'Bull      ') & \
                                        (cbbc_data['Underlying'] == underlying_asset) & \
                                        (cbbc_data['Trade Date'] == trade_date)]
                if underlying_asset == 'HSI' or 'HSCEI':
                    bull_datum['hedging_volume'] = bull_datum['No. of CBBC still out in market *'] / bull_datum['Ent. Ratio^'] / 50
                else:
                    bull_datum['hedging_volume'] = bull_datum['No. of CBBC still out in market *'] / bull_datum['Ent. Ratio^']

                bull_datum['chips_amount'] = bull_datum['Closing Price'] * bull_datum['No. of CBBC still out in market *']
                
                bull_hedge_volume = bull_datum['hedging_volume'].sum()
                bull_chips_amount = bull_datum['chips_amount'].sum()


                # Bear part
                bear_datum = cbbc_data[(cbbc_data['Bull/Bear'] == 'Bear      ') & \
                                        (cbbc_data['Underlying'] == underlying_asset) & \
                                        (cbbc_data['Trade Date'] == trade_date)]
                if underlying_asset == 'HSI' or 'HSCEI':
                    bear_datum['hedging_volume'] = bear_datum['No. of CBBC still out in market *'] / bear_datum['Ent. Ratio^'] / 50
                else:
                    bear_datum['hedging_volume'] = bear_datum['No. of CBBC still out in market *'] / bear_datum['Ent. Ratio^']

                bear_datum['chips_amount'] = bear_datum['Closing Price'] * bear_datum['No. of CBBC still out in market *']
                
                bear_hedge_volume = bear_datum['hedging_volume'].sum()
                bear_chips_amount = bear_datum['chips_amount'].sum()

                # meta data
                trade_date_obj = datetime.strptime(trade_date, '%Y-%m-%d')
                scrape_date = datetime.now()
                stock_abbv = underlying_asset.lstrip("0")
                try:
                    if not bull_datum.empty:
                        cbbc_abbv = bull_datum['CBBC Name'].iloc[0][3:8].rstrip()
                    else:
                        cbbc_abbv = bear_datum['CBBC Name'].iloc[0][3:8].rstrip()
                except:
                    continue
            
                stock_obj, created = StockSchema.objects.get_or_create(stock_abbv=stock_abbv, defaults=dict(status='A', is_index=False, cbbc_abbv=cbbc_abbv))

                # bull bear ratio calculation
                if bull_hedge_volume == 0 and bear_hedge_volume == 0:
                    bull_bear_ratio_for_hedge_volume = 0
                else:
                    bull_bear_ratio_for_hedge_volume = bull_hedge_volume / (bull_hedge_volume + bear_hedge_volume)
                
                if bull_chips_amount == 0 and bear_chips_amount == 0:
                    bull_bear_ratio_for_chips = 0
                else:
                    bull_bear_ratio_for_chips = bull_chips_amount / (bull_chips_amount + bear_chips_amount)

                # Get close price by yahoo finance API
                try:
                    close_price = get_close_price(trade_date, underlying_asset)
                except:
                    close_price = -1


                # integrate the data
                bull_bear_data = dict(status='A', scrape_datetime=scrape_date, bull_hedge_volume=bull_hedge_volume,
                                        bear_hedge_volume=bear_hedge_volume, bull_bear_ratio_for_hedge_volume=bull_bear_ratio_for_hedge_volume,
                                        bull_chips_amount=bull_chips_amount, bear_chips_amount=bear_chips_amount,
                                        bull_bear_ratio_for_chips=bull_bear_ratio_for_chips, close_price=close_price)
                BullBearRatioSchema.objects.update_or_create(stock=stock_obj, trade_date=trade_date_obj, defaults=bull_bear_data)
        os.remove(filename)