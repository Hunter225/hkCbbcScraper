from datetime import datetime
import requests
import constants
import zipfile
import os

def main():
    this_month = datetime.today().strftime("%m")
    url = constants.CBBC_zip_download_link_template(this_month)
    r = requests.get(url, stream=True)
    zip_file_path = constants.save_dir_of_CBBC_data + url.split('/')[-1]

    with open(zip_file_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(constants.save_dir_of_CBBC_data)

    os.remove(zip_file_path)