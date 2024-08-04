import requests
import json

#Primer paso, se hace la consulta a la API para obtener el Token y se almacena en un .txt

# URL de la API para obtener el token
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
    # Obtener la respuesta JSON
    response_json = response.json()
    
    # Extraer el refreshToken
    refresh_token = response_json.get('refreshToken')
    
    # Guardar el refreshToken en un archivo de texto
    with open('refresh_token.txt', 'w') as file:
        file.write(refresh_token)
    
    print("Refresh Token almacenado en refresh_token.txt")

else:
    # Si hubo un error, imprimir el estado y el contenido de la respuesta
    print(f"Error: {response.status_code}")
    print("Contenido de la respuesta:", response.text)


#Segundo Paso
#Prueba que lee el archivo que se guardo dentro del txt

# Nombre del archivo donde se almacenó el refreshToken
file_name = 'refresh_token.txt'

try:
    # Abrir el archivo en modo de lectura
    with open(file_name, 'r') as file:
        # Leer el contenido del archivo
        refresh_token = file.read().strip()  # Usar strip() para eliminar posibles espacios en blanco
        
        # Imprimir el refreshToken leído
        print("Refresh Token leído desde el archivo:")
        print(refresh_token)

except FileNotFoundError:
    print(f"El archivo {file_name} no se encontró.")
except IOError as e:
    print(f"Se produjo un error al leer el archivo: {e}")




