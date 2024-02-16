import requests

# все пароли и токены не должны быть в коде и должны храниться в отдельном файле
from dotenv import load_dotenv
import os

load_dotenv()
RapidAPIKey = os.getenv('RapidAPIKey')

url = "https://matchilling-chuck-norris-jokes-v1.p.rapidapi.com/jokes/random"

headers = {
	"accept": "application/json",
	"X-RapidAPI-Key": RapidAPIKey,
	"X-RapidAPI-Host": "matchilling-chuck-norris-jokes-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())