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

# Objeto con credenciales para conexión SAND o PROD
ppiCredentials = {
    "SAND": {
        "baseUrl": "https://clientapi_sandbox.portfoliopersonal.com/",
        "authorizedClient": "API_CLI_REST",
        "clientKey": "ppApiCliSB"
    },
    "PROD": {
        "baseUrl": "https://clientapi.portfoliopersonal.com/",
        "authorizedClient": "API_CLI_REST",
        "clientKey": "pp19CliApp12"
    }
}

############################### Funciones Locales ###############################
#### Definir en esta ubicación todas las funciones que utilizarán localmente ####
#################################################################################

def getCredentials(sandEnvironment, method):
    # Base URL con metodo a utilizar
    baseUrl = ppiCredentials["SAND"]["baseUrl"] if sandEnvironment else ppiCredentials["PROD"]["baseUrl"]
    # Credenciales ppi segun ambiente seleccionado
    credentials = {
        "authorizedClient": ppiCredentials["SAND"]["authorizedClient"] if sandEnvironment else ppiCredentials["PROD"]["authorizedClient"],
        "clientKey": ppiCredentials["SAND"]["clientKey"] if sandEnvironment else ppiCredentials["PROD"]["clientKey"],        
        "url" : baseUrl + method
    }
    return credentials 

############################### Execute index HTML page ###############################

@app.route('/')
def index():
    return render_template('index.html')
    
############################### Log in function ###############################

@app.route('/LoginApi', methods=['POST'])
def get_login():
    # Se cargan variables en base a campos en HTML
    publicKey = request.json.get('public_key')
    privateKey = request.json.get('private_key')
    isSandEnvironment = request.json.get('ambiente_sand')
    app.logger.info(publicKey)
    app.logger.info(privateKey)
    app.logger.info(isSandEnvironment)
    credentials = getCredentials(request.json.get('ambiente_sand'), "api/1.0/Account/LoginApi")
    
    app.logger.info(credentials["authorizedClient"])
    app.logger.info(credentials["clientKey"])
    app.logger.info(credentials["url"])
    headers = {
        "AuthorizedClient": credentials["authorizedClient"],
        "ClientKey": credentials["clientKey"],
        "Content-Type": "application/json",
        "ApiKey": publicKey,
        "ApiSecret": privateKey
    }

    data = {}

    response = requests.post(credentials["url"], headers=headers, data=json.dumps(data), verify=False)

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
    isSandEnvironment = request.json.get('ambiente_sand')
    app.logger.info(isSandEnvironment)
    credentials = getCredentials(request.json.get('ambiente_sand'), "api/1.0/Account/RefreshToken")

    headers = {
        "AuthorizedClient": credentials["authorizedClient"],
        "ClientKey": credentials["clientKey"],
        "Content-Type": "application/json",
        "Authorization": "Bearer " + stored_refresh_token
    }

    data = {
        "refreshToken": stored_refresh_token
    }

    app.logger.info(credentials["authorizedClient"])
    app.logger.info(credentials["clientKey"])
    app.logger.info(credentials["url"])

    response = requests.post(credentials["url"], headers=headers, data=json.dumps(data), verify=False)

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

@app.route('/get_accounts', methods=['POST'])
def get_accounts():
    isSandEnvironment = request.json.get('ambiente_sand')
    app.logger.info(isSandEnvironment)
    credentials = getCredentials(request.json.get('ambiente_sand'), "api/1.0/Account/Accounts")

    app.logger.info(credentials["authorizedClient"])
    app.logger.info(credentials["clientKey"])
    app.logger.info(credentials["url"])

    headers = {
        "AuthorizedClient": credentials["authorizedClient"],
        "ClientKey": credentials["clientKey"],
        "Content-Type": "application/json",
        "Authorization": "Bearer " + stored_access_token
    }

    response = requests.get(credentials["url"], headers=headers, verify=False)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error en la solicitud', 'status_code': response.status_code, 'response': response.text})
    
    ############################### Info Movements ###############################

@app.route('/get_account_movements', methods=['POST'])
def get_account_movements():
    isSandEnvironment = request.json.get('ambiente_sand')
    accountNumber = request.json.get('accounts')
    app.logger.info(isSandEnvironment)
    datefrom = request.json.get('date_from')
    dateTo = request.json.get('date_to')
    ticker = request.json.get('ticker')
    getMovementsUrl = "api/1.0/Account/Movements?accountNumber="+accountNumber+"&dateFrom="+datefrom+"&dateTo="+dateTo+"&ticker="+ticker    
    app.logger.info(getMovementsUrl)
    credentials = getCredentials(request.json.get('ambiente_sand'), getMovementsUrl)

    app.logger.info(credentials["authorizedClient"])
    app.logger.info(credentials["clientKey"])
    app.logger.info(credentials["url"])

    headers = {
        "AuthorizedClient": credentials["authorizedClient"],
        "ClientKey": credentials["clientKey"],
        "Content-Type": "application/json",
        "Authorization": "Bearer " + stored_access_token
    }

    response = requests.get(credentials["url"], headers=headers, verify=False)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error en la solicitud', 'status_code': response.status_code, 'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)