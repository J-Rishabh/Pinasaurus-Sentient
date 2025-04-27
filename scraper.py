
# given an amazon link will get the product name, the photo and description.

import requests
import json
from bs4 import BeautifulSoup

url = "https://www.amazon.com/Bluetooth-Portable-Wireless-Speakers-Accessories/dp/B09LQJBCT7?sr=8-2"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

print(soup.prettify())