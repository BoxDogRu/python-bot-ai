# pip install python-dotenv

from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('TOKEN')
