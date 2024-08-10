from flask import Flask, jsonify, render_template, request
import requests
import json

app = Flask(__name__)

# Variables globales
global authorizedClient
global clientKey
global apiKey
global apiSecret
# Variables globales para almacenar tokens
stored_refresh_token = None
stored_access_token = None

# Cambiar a False y completar con credenciales para PROD
SANDconnected = False

if SANDconnected:
    baseUrl = "https://clientapi_sandbox.portfoliopersonal.com/"
    authorizedClient = "API_CLI_REST"
    clientKey = "ppApiCliSB"
    apiKey = "VHltelE1SG5EOGZrdndzdE5ZMU4="
    apiSecret = "MjA3MDBhNzItNmMzOC00YzRhLWIyMzQtOGUwNGYyODY3ZWY0"
else:
    baseUrl = "https://clientapi.portfoliopersonal.com/"
    authorizedClient = "API_CLI_REST"
    clientKey = "pp19CliApp12"
    apiKey = ""
    apiSecret = ""

############################### Execute index HTML page ###############################

@app.route('/')
def index():
    return render_template('index.html')

############################### Get Token function ###############################

@app.route('/get_refresh_token')
def get_refresh_token():
    url = baseUrl + "api/1.0/Account/LoginApi"

    headers = {
        "AuthorizedClient": authorizedClient,
        "ClientKey": clientKey,
        "Content-Type": "application/json",
        "ApiKey": apiKey,
        "ApiSecret": apiSecret
    }

    data = {}

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        response_json = response.json()
        refresh_token = response_json.get('refreshToken')
        global stored_refresh_token
        stored_refresh_token = refresh_token
        if refresh_token:
            return jsonify({'refreshToken': refresh_token})
        else:
            return jsonify({'error': 'No se encontró el refreshToken en la respuesta.'})
    else:
        return jsonify({'error': 'Error en la solicitud', 'status_code': response.status_code, 'response': response.text})

############################### Refresh access token function ###############################

@app.route('/refresh_access_token', methods=['POST'])
def refresh_access_token():
    url = baseUrl + "api/1.0/Account/RefreshToken"

    headers = {
        "AuthorizedClient": authorizedClient,
        "ClientKey": clientKey,
        "Content-Type": "application/json",
        "Authorization": "Bearer " + stored_refresh_token
    }

    data = {
        "refreshToken": stored_refresh_token
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json.get('accessToken')
        global stored_access_token
        stored_access_token = access_token
        if access_token:
            return jsonify({'accessToken': access_token})
            
        else:
            return jsonify({'error': 'No se encontró el accessToken en la respuesta.'})
    else:
        return jsonify({'error': 'Error en la solicitud', 'status_code': response.status_code, 'response': response.text})


############################### Info Account ###############################

@app.route('/get_accounts')
def get_accounts():
    if stored_access_token is None:
        return jsonify({'error': 'No access token available.'})

    url = baseUrl + "api/1.0/Account/Accounts"

    headers = {
        "AuthorizedClient": authorizedClient,
        "ClientKey": clientKey,
        "Content-Type": "application/json",
        "Authorization": "Bearer " + stored_access_token
    }

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error en la solicitud', 'status_code': response.status_code, 'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)

#Se almaceno la variable Access Token en stored_access_token

#Se crea un nuevo boton en html: <button onclick="fetchAccounts()">Obtener Cuentas</button>

#Se crea la referencia en JS:
#  function fetchAccounts() {
    #if (window.accessToken) {
    #   fetch('/get_accounts')

#Esto llama a py donde se colocaron los parametros de URL, Header, llamando a Autorizathion como stored_access_token

#revise en la terminar del boton HTML que trae la info y tira:
    #ReferenceError: fetchAccounts is not defined
    #pero el boton lo veo bien vinculado a JS.
    #Siento que es una boludes
    
