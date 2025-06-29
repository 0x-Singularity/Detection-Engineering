import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://c1f15cbeea394929ad06f29bf0b1d3ac.us-east4.gcp.elastic-cloud.com/api/detection_engine/rules"
api_key = os.getenv("API_KEY")
headers = {
    'Content-Type': 'application/json;chatset=UTF-8',
    'kbn-xsrf': 'true',
    'Authorization': 'ApiKey ' + api_key
}

data = """
    
"""

elastic_data = requests.post(url, headers=headers, data=data).json()