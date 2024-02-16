import requests

# все пароли и токены не должны быть в коде и должны храниться в отдельном файле
from dotenv import load_dotenv
import os

load_dotenv()
RapidAPIKey = os.getenv('RapidAPIKey')

url = "https://numbersapi.p.rapidapi.com/1/21/date"

querystring = {"fragment":"true","json":"true"}

headers = {
	"X-RapidAPI-Key": RapidAPIKey,
	"X-RapidAPI-Host": "numbersapi.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())