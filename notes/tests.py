from datetime import datetime
import requests as request
from getpass import getpass
import json

endpoint = "http://127.0.0.1:8000/auth/login/"

email = input("Email:")
#password = getpass("Votre mot de passe: ")

# data for the authentication
data = {
   "password": "ge",
   "email":email
}


# data = json.dumps(data)

# only post can be use to obtain the token
get_response = request.post(endpoint, data=data)

# headers configuration : ajouter pour n'import quelle autre request

token = get_response.json()["tokens"]["access"]
headers = {
    "Authorization" : f"Bearer {token}"
}


if get_response.status_code ==200:
    endpoint = "http://127.0.0.1:8000/notes/audio/mark/"

    get_exo =  request.get(endpoint, headers=headers)
    print(get_exo.json())
