import requests
import json

def search_mouser_parts(api_key, version, keyword, records, starting_record, search_options, search_language):
    url = f"https://api.mouser.com/api/{version}/search/keyword"
    
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "SearchByKeywordRequest": {
            "keyword": keyword,
            "records": records,
            "startingRecord": starting_record,
            "searchOptions": search_options,
            "searchWithYourSignUpLanguage": search_language
        }
    }
    response = requests.post(url, headers=headers, json=payload, params={"apiKey": api_key})
    if response.status_code == 200:
        return response.json()
    else:
        return response.text

# Example usage
api_key = "891a3cf6-13e6-495a-8789-c12e0c17e685"
version = "V1"
keyword = "resistor"
records = 1
starting_record = 0
search_options = "RohsAndInStock"
search_language = "en"

results = search_mouser_parts(api_key, version, keyword, records, starting_record, search_options, search_language)
print(json.dumps(results, indent=4))
