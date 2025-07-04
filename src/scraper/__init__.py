from geopy.geocoders import Nominatim
import requests
from urllib.parse import quote
from datetime import datetime
import os
import subprocess

class Scraper:
    def __init__(self, location: str, start_date: str = 'JUN/4/2025', end_date: str = 'JUL/4/2025'):
        self.location = location
        self.start_date = start_date
        self.end_date = end_date

        geolocator = Nominatim(user_agent='myapplication')
        location_data = geolocator.geocode(self.location)
        if location_data:
            self.latitude = location_data.latitude
            self.longitude = location_data.longitude
        else:
            raise ValueError("Location not found")

    def build_encoded_raw_data(self):
        satellites = 'ResourceSat-2A_LISS3_L2,Sentinel-2A_MSI_Level-2A'

        payload = {
            "userId": "T",
            "prod": "Standard",
            "selSats": quote(satellites),
            "offset": "0",
            "sdate": quote(self.start_date),
            "edate": quote(self.end_date),
            "query": "area",
            "queryType": "location",
            "isMX": "No",
            "loc": "Decimal",
            "lat": f"{self.latitude:.4f}",
            "lon": f"{self.longitude:.4f}",
            "radius": "10",
            "filters": quote("{}")
        }

        raw_data = (
            '{'
            f'"userId":"{payload["userId"]}",'
            f'"prod":"{payload["prod"]}",'
            f'"selSats":"{payload["selSats"]}",'
            f'"offset":"{payload["offset"]}",'
            f'"sdate":"{payload["sdate"]}",'
            f'"edate":"{payload["edate"]}",'
            f'"query":"{payload["query"]}",'
            f'"queryType":"{payload["queryType"]}",'
            f'"isMX":"{payload["isMX"]}",'
            f'"loc":"{payload["loc"]}",'
            f'"lat":"{payload["lat"]}",'
            f'"lon":"{payload["lon"]}",'
            f'"radius":"{payload["radius"]}",'
            f'"filters":"{payload["filters"]}"'
            '}'
        )

        return raw_data

    def get_images(self):
        url = 'https://bhoonidhi.nrsc.gov.in/bhoonidhi/ProductSearch'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Referer': 'https://bhoonidhi.nrsc.gov.in/bhoonidhi/index.html',
            'Content-Type': 'application/json',
            'token': '',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://bhoonidhi.nrsc.gov.in',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=3315237696C5CFA2449CD3452F6BC677; JSESSIONID=C607D5808BCC74001F73D8E2616F8107',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=0'
        }

        raw_data = self.build_encoded_raw_data()
        response = requests.post(url, headers=headers, data=raw_data)

        if response.status_code == 200:
            return response.json()['Results']
        else:
            print("Error:", response.status_code, response.text)
            return None

    def download_image(self, image_data):
        base_url = 'http://bhoonidhi.nrsc.gov.in'
        dir_path = image_data.get('DIRPATH')
        filename = image_data.get('FILENAME', 'downloaded_image').strip()

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            "Referer": "https://bhoonidhi.nrsc.gov.in",
        }

        if not dir_path:
            print("Missing DIRPATH in image data.")
            return

        complete_url = f"{base_url}{dir_path}{filename}.jpg"
        print(f"URL: {complete_url}")
        output_path = "images/"
        subprocess.run(["wget", "-P", output_path, complete_url])
