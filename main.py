from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='myapplication')
location = geolocator.geocode("New Delhi, India")
print(location.raw['lat'])
print(location.raw['lon'])

# curl 'https://bhoonidhi.nrsc.gov.in/bhoonidhi/ProductSearch' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br, zstd' -H 'Referer: https://bhoonidhi.nrsc.gov.in/bhoonidhi/index.html' -H 'Content-Type: application/json' -H 'token: ' -H 'X-Requested-With: XMLHttpRequest' -H 'Origin: https://bhoonidhi.nrsc.gov.in' -H 'Sec-GPC: 1' -H 'Connection: keep-alive' -H 'Cookie: JSESSIONID=3315237696C5CFA2449CD3452F6BC677; JSESSIONID=C607D5808BCC74001F73D8E2616F8107' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'Priority: u=0' --data-raw '{"userId":"T","prod":"Standard","selSats":"ResourceSat-2A_LISS3_L2%2CSentinel-2A_MSI_Level-2A","offset":"0","sdate":"JUN%2F4%2F2025","edate":"JUL%2F4%2F2025","query":"area","queryType":"location","isMX":"No","loc":"Decimal","lat":"28.6430","lon":"77.2192","radius":"10","filters":"%7B%7D"}'
import requests

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

raw_data = '{"userId":"T","prod":"Standard","selSats":"ResourceSat-2A_LISS3_L2%2CSentinel-2A_MSI_Level-2A","offset":"0","sdate":"JUN%2F4%2F2025","edate":"JUL%2F4%2F2025","query":"area","queryType":"location","isMX":"No","loc":"Decimal","lat":"28.6430","lon":"77.2192","radius":"10","filters":"%7B%7D"}'

response = requests.post(url, headers=headers, data=raw_data)

print(response.status_code)
print(response.text)

