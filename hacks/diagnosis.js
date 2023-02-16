import requests

url = "https://medius-disease-medication.p.rapidapi.com/api/v2/disease-medications/E_0000017290"

querystring = {"country":"IN"}

headers = {
	"X-RapidAPI-Key": "b3323bf068msh78fdc9a03f97535p1332dcjsnfe5d256eaa9a",
	"X-RapidAPI-Host": "medius-disease-medication.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

json = response.json()