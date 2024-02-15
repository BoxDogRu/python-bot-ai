# https://rapidapi.com/fyhao/api/currency-exchange/ документация

import requests

# все пароли и токены не должны быть в коде и должны храниться в отдельном файле
from dotenv import load_dotenv
import os

load_dotenv()
RapidAPIKey = os.getenv('RapidAPIKey')

# 1. Список валют
url_listquotes = "https://currency-exchange.p.rapidapi.com/listquotes"

headers = {
	"X-RapidAPI-Key": RapidAPIKey,
	"X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
}

response = requests.get(url_listquotes, headers=headers)
print(response.json())


# 2. Обмен валюты
url = "https://currency-exchange.p.rapidapi.com/exchange"

headers = {
	"X-RapidAPI-Key": RapidAPIKey,
	"X-RapidAPI-Host": "currency-exchange.p.rapidapi.com"
}

querystring = {"from":"EUR","to":"RUB","q":"1.0"}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
