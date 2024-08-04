
import requests
import json

# URL de la API
url = "https://clientapi_sandbox.portfoliopersonal.com/api/1.0/Account/LoginApi"

# Encabezados necesarios para la solicitud
headers = {
    "AuthorizedClient": "API_CLI_REST",
    "ClientKey": "ppApiCliSB",
    "Content-Type": "application/json",
    "ApiKey": "VHltelE1SG5EOGZrdndzdE5ZMU4=",
    "ApiSecret": "MjA3MDBhNzItNmMzOC00YzRhLWIyMzQtOGUwNGYyODY3ZWY0"
}

# Datos del cuerpo de la solicitud (si se requiere algún dato en el cuerpo, debe añadirse aquí)
data = {}  # Deja esto vacío si no se necesitan datos en el cuerpo

# Realizar la solicitud POST
response = requests.post(url, headers=headers, data=json.dumps(data))

# Verificar el estado de la respuesta
if response.status_code == 200:
    # Si la solicitud fue exitosa, imprimir la respuesta JSON
    print("Solicitud exitosa.")
    print("Respuesta JSON:", response.json())
else:
    # Si hubo un error, imprimir el estado y el contenido de la respuesta
    print(f"Error: {response.status_code}")
    print("Contenido de la respuesta:", response.text)