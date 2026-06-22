import requests

url = "https://api.github.com/trending"

print("Growth Radar AI")
print("Checking internet connection...")

response = requests.get("https://api.github.com")

print("Status Code:", response.status_code)

if response.status_code == 200:
    print("Internet connection working!")
else:
    print("Something went wrong.")
