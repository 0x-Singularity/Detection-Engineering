import requests
from dotenv import load_dotenv
import os
import tomllib

load_dotenv()

url = "https://c1f15cbeea394929ad06f29bf0b1d3ac.us-east4.gcp.elastic-cloud.com/api/detection_engine/rules"
api_key = os.getenv("API_KEY")
headers = {
    'Content-Type': 'application/json;chatset=UTF-8',
    'kbn-xsrf': 'true',
    'Authorization': 'ApiKey ' + api_key
}

data = ""

for root, dirs, files in os.walk("custom-detection-rules/"):
    for file in files:
        data = "{\n"
        if file.endswith(".toml"):
            full_path = os.path.join(root, file)
            with open(full_path,"rb") as toml:
                alert = tomllib.load(toml)

            if alert['rule']['type'] == "query": # query based alert
                required_fields = ['author','description', 'name','rule_id','risk_score','severity','type','query','threat']
            elif alert['rule']['type'] == "eql": # event correlation alert
                required_fields = ['author','description', 'name','rule_id','risk_score','severity','type','query','language','threat']
            elif alert['rule']['type'] == "threshold": # threshold based alert
                required_fields = ['author','description', 'name','rule_id','risk_score','severity','type','query','threshold','threat']
            else:
                print("Unsupported rule type found in: " + full_path)
                break
            
            for field in alert['rule']:
                if field in required_fields:
                    if type(alert['rule'][field]) == list:
                        data += "  " + "\"" + field + "\": " + str(alert['rule'][field]).replace("'","\"") + "," + "\n"
                    elif type(alert['rule'][field]) == str:
                        if field == 'description':
                            data += "  " + "\"" + field + "\": \"" + str(alert['rule'][field]).replace("\n"," ").replace("\"","\\\"").replace("\\","\\\\") + "\"," + "\n"
                        elif field == 'query':
                            data += "  " + "\"" + field + "\": \"" + str(alert['rule'][field]).replace("\\","\\\\").replace("\"","\\\"").replace("\n"," ") + "\"," + "\n"
                        else:
                            data += "  " + "\"" + field + "\": \"" + str(alert['rule'][field]).replace("\n"," ").replace("\"","\\\"") + "\"," + "\n"
                    elif type(alert['rule'][field]) == int:
                        data += "  " + "\"" + field + "\": " + str(alert['rule'][field]) + "," + "\n"
                    elif type(alert['rule'][field]) == dict:
                        data += "  " + "\"" + field + "\": " + str(alert['rule'][field]).replace("'","\"") + "," + "\n"
                    
            data += "  \"enabled\": true\n}"

        elastic_data = requests.post(url, headers=headers, data=data).json()
        print(elastic_data)