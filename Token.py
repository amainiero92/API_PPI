from flask import Flask, jsonify, render_template, request
import requests
import json

app = Flask(__name__)

# Variable global para almacenar el refreshToken
stored_refresh_token = None

############################### Execute index HTML page ###############################

@app.route('/')
def index():
    return render_template('index.html')

############################### Get Token function ###############################

@app.route('/get_refresh_token')
def get_refresh_token():
    url = "https://clientapi_sandbox.portfoliopersonal.com/api/1.0/Account/LoginApi"

    headers = {
        "AuthorizedClient": "API_CLI_REST",
        "ClientKey": "ppApiCliSB",
        "Content-Type": "application/json",
        "ApiKey": "VHltelE1SG5EOGZrdndzdE5ZMU4=",
        "ApiSecret": "MjA3MDBhNzItNmMzOC00YzRhLWIyMzQtOGUwNGYyODY3ZWY0"
    }

    data = {}

    # Parametro verify se setea en falso para evitar el uso de un certificado. No recomendado en ambiente productivo
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
    url = "https://clientapi_sandbox.portfoliopersonal.com/api/1.0/Account/RefreshToken"

    headers = {
        "AuthorizedClient": "API_CLI_REST",
        "ClientKey": "ppApiCliSB",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + stored_refresh_token
    }

    data = {
        "refreshToken": stored_refresh_token
    }

    # Parametro verify se setea en falso para evitar el uso de un certificado. No recomendado en ambiente productivo
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Error en la solicitud de refresco', 'status_code': response.status_code, 'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)