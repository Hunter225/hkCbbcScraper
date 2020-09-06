from datetime import datetime
import requests
import constants
import zipfile
import os
from scripts.parse_hkex_cbbc_csv import main as parse_hkex_cbbc_csv
from scripts.download_hkex_cbbc_data import main as download_cbbc_data

def run():
    download_cbbc_data()
    parse_hkex_cbbc_csv()