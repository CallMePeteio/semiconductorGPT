



accessToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjA5NzI5QTkyRDU0RDlERjIyRDQzMENBMjNDNkI4QjJFIiwidHlwIjoiYXQrand0In0.eyJuYmYiOjE3MDAzMzk1NDYsImV4cCI6MTcwMDQyNTk0NiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS5uZXhhci5jb20iLCJjbGllbnRfaWQiOiI5OGYxNTk5ZS1iN2JlLTQwNmEtYTI3MC0yN2VlMmI3ZjgxNTQiLCJzdWIiOiI4Qzk5MEFDQS00NDY4LTREOEYtOTc4My03QzE3MzRCNkFFOTUiLCJhdXRoX3RpbWUiOjE3MDAzMzkxODksImlkcCI6ImxvY2FsIiwicHJpdmF0ZV9jbGFpbXNfaWQiOiJmNjNiMjQxMS00ZGNmLTQyZDQtYjA4NC02MDBiNzBlMzdiMmUiLCJwcml2YXRlX2NsYWltc19zZWNyZXQiOiJaRXgwM2hsWllqZTZaNW9NTlZJc0hOaS94NWJKaWZnVUZXZmRsRmxSelkwPSIsImp0aSI6IjY2QkJDNjc2RTNCREVBMUVENjRFRTMxNjk1QzdFMzdGIiwic2lkIjoiNDE2NkEyNTIwQzM4OTREODQ5MTYzMDc1NjY1M0RFQTkiLCJpYXQiOjE3MDAzMzk1NDYsInNjb3BlIjpbIm9wZW5pZCIsInVzZXIuYWNjZXNzIiwicHJvZmlsZSIsImVtYWlsIiwidXNlci5kZXRhaWxzIiwic3VwcGx5LmRvbWFpbiIsImRlc2lnbi5kb21haW4iXSwiYW1yIjpbInB3ZCJdfQ.eLFqvhjcs3Frk8lA0rjVLTFiGjyAKv1swYUtEcB4LVm8o_T9fiu4VwidmxiKP3v_MvQkOxRw4Ae0f64xfq-5GAAuq8VjFpBW6qztlY5A6Txh3e3CPrVBHdBsd_kO-qnQSyLXKzOJUg9T34cwoNADK-WQsTDuYzEmwLK6r_g636ZkJh0ecmYvLkHAe2VQIBCt-UnbBJMmTIV7F_hZCtxh_ZQjEoYKMUll1b2kNzTerLJh4VZwj20yoDOGHeUNB5p6Qovbknbdq9xLaIhXVnDK_2d8L9Ski2_9JJEgUOAC1jHIxVHW99cpjhEclY6WkIla5WjdqAF2RVXH3pKieB6PyA"
clientId = "98f1599e-b7be-406a-a270-27ee2b7f8154"
clientSecret = "wbedA1v2AAIs595ABRlCXkzoYBpNBaSHhuCv"


import requests

# API endpoint
url = "https://octopart.com/api/v3/parts/match"

# Your API key
api_key = accessToken

# The part you are querying
part_query = '[{"mpn":"SN74S74N"}]'

# Include different data types in the request
include_data = [
    "datasheets",
    "compliance_documents",
    "cad_models",
    "descriptions",
    "specs",
    "imagesets"
]

# Parameters for the API request
params = {
    "apikey": api_key,
    "queries": part_query,
    "include[]": include_data
    

}

# Making the GET request
response = requests.get(url, params=params)

# Check if the request was successful

# Process the response
data = response.json()
print(data)
