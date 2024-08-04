import requests

#Solicitud de Token a Broker "IOL"
def pedirToken():
    url='https://clientapi_sandbox.portfoliopersonal.com/api/1.0/Account/LoginApi'
    data= {"AuthorizedClient": "API_CLI_REST", "ClientKey":"ppApiCliSB",
           "Content-Type":"application/json","ApiKey":"VHltelE1SG5EOGZrdndzdE5ZMU4=",
             "ApiSecret":"MjA3MDBhNzItNmMzOC00YzRhLWIyMzQtOGUwNGYyODY3ZWY0"}
    r= requests.post(url=url ,data=data ).json()
    return r

tk= pedirToken() 

