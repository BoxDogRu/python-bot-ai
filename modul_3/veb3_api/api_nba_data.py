import requests

# все пароли и токены не должны быть в коде и должны храниться в отдельном файле
from dotenv import load_dotenv
import os

load_dotenv()
RapidAPIKey = os.getenv('RapidAPIKey')

url = "https://free-nba.p.rapidapi.com/players"

querystring = {"page":"0","per_page":"25"}

headers = {
	"X-RapidAPI-Key": RapidAPIKey,
	"X-RapidAPI-Host": "free-nba.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())