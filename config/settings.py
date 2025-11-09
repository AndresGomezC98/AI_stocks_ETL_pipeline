# Using the Os library and dotenv
from dotenv import load_dotenv
import os
# load_dotenv is used to automatically read the key-values ​​from the project's .env file and place them in the os.env file.
load_dotenv()
# We use the os.getenv module to get the values of api key, and database managment of os.env
AV_API_KEY:str= os.getenv('AV_API_KEY')

if AV_API_KEY is None:
    raise Exception('the KEY API wasnt found, please check the .env document to change and update KEY API to proper connection')

DB_HOST:str= os.getenv('DB_HOST')
DB_USER: str = os.getenv('DB_USER')
DB_PASSWORD:str = os.getenv('DB_PASSWORD')
DB_DATABASE: str= os.getenv('DB_DATABASE')

# We create a list of our ten main stocks of AI to follow with API 

AI_TICKERS:list[str]=[ 'NVDA', 'MSFT', 'AMD', 'PLTR', 'META', 'GOOGL', 'ADBE', 'TSLA', 'AMZN', 'BRK.B']
