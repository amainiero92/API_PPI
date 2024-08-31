import requests
from datetime import datetime, timedelta
import pandas as pd

# Definir variables
casa = "blue"  # oficial, blue, bolsa, cripto, mayorista, solidario, turista
#fecha_inicio = "2024/08/20"  # Fecha de inicio en formato YYYY/MM/DD
#fecha_fin = "2024/08/30"  # Fecha de fin en formato YYYY/MM/DD

# Convertir las cadenas de fecha a objetos datetime
#fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y/%m/%d")
#fecha_fin_dt = datetime.strptime(fecha_fin, "%Y/%m/%d")

#Cambio el codigo y le digo que traiga los ultimos xx dias desde ayer
fecha_fin_dt = datetime.now() - timedelta(days=1) #Hasta hoy -1
fecha_inicio_dt = fecha_fin_dt - timedelta(days=30) #Desde Hoy -10

# Crear una lista para almacenar los datos
datos = []

# Iterar sobre cada día en el rango de fechas
current_date = fecha_inicio_dt
while current_date <= fecha_fin_dt:
    # Convertir la fecha actual al formato adecuado para la URL
    fecha_str = current_date.strftime("%Y/%m/%d")
    
    # Construir la URL para la fecha actual
    url = f"https://api.argentinadatos.com/v1/cotizaciones/dolares/{casa}/{fecha_str}"
    
    # Hacer la solicitud GET
    response = requests.get(url)
    data = response.json()
    
    # Agregar los datos a la lista
    if response.status_code == 200:
        datos.append({
            "Fecha": fecha_str,
            "Casa": data.get("casa"),
            "Compra": data.get("compra"),
            "Venta": data.get("venta")
            
        })
    else:
        datos.append({
            "Fecha": fecha_str,
            "Compra": None,
            "Venta": None,
            "Casa": None
        })
    
    # Avanzar al siguiente día
    current_date += timedelta(days=1)

# Crear un DataFrame con los datos recopilados
df = pd.DataFrame(datos)

# Mostrar la tabla
print(df)
