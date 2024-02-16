import requests

# все пароли и токены не должны быть в коде и должны храниться в отдельном файле
from dotenv import load_dotenv
import os

load_dotenv()
RapidAPIKey = os.getenv('RapidAPIKey')

url = "https://love-calculator.p.rapidapi.com/getPercentage"

querystring = {"sname":"Николай","fname":"Алиса"}

headers = {
	"X-RapidAPI-Key": RapidAPIKey,
	"X-RapidAPI-Host": "love-calculator.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())