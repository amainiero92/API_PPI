from flask import Flask, jsonify, render_template, request
import requests
import json
import string
import secrets

app = Flask(__name__)

# Variables globales
global authorizedClient
global clientKey
global apiKey
global apiSecret

# Variables globales para almacenar tokens
stored_refresh_token = None
stored_access_token = None
apiKey = ""
apiSecret = ""

# Cambiar a False y completar con credenciales para PROD
SANDconnected = True

if SANDconnected:
    baseUrl = "https://clientapi_sandbox.portfoliopersonal.com/"
    authorizedClient = "API_CLI_REST"
    clientKey = "ppApiCliSB"
else:
    baseUrl = "https://clientapi.portfoliopersonal.com/"
    authorizedClient = "API_CLI_REST"
    clientKey = "pp19CliApp12"

############################### Execute index HTML page ###############################

@app.route('/')
def index():
    return render_template('index.html')
    
############################### Log in function ###############################

@app.route('/LoginApi', methods=['POST'])
def get_login():
    publicKey = request.json.get('public_key')
    privateKey = request.json.get('private_key')
    url = baseUrl + "api/1.0/Account/LoginApi"

    app.logger.info(publicKey)
    app.logger.info(privateKey)
    headers = {
        "AuthorizedClient": authorizedClient,
        "ClientKey": clientKey,
        "Content-Type": "application/json",
        "ApiKey": publicKey,
        "ApiSecret": privateKey
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