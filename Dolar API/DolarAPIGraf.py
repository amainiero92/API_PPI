import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# Definir variables
casa = "blue"  # oficial, blue, bolsa, cripto, mayorista, solidario, turista

# Calcular las fechas
fecha_fin_dt = datetime.now() - timedelta(days=1)  # Hasta hoy -1
fecha_inicio_dt = fecha_fin_dt - timedelta(days=30)  # Desde hoy -30

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

# Convertir la columna de fechas a datetime
df['Fecha'] = pd.to_datetime(df['Fecha'], format="%Y/%m/%d")

# Ordenar el DataFrame por fecha
df.sort_values('Fecha', inplace=True)

# Graficar la evolución de las cotizaciones
plt.figure(figsize=(10, 5))

# Graficar la compra y venta
plt.plot(df['Fecha'], df['Compra'], label='Compra', marker='o', color='green')
plt.plot(df['Fecha'], df['Venta'], label='Venta', marker='o', color='red')

# Añadir detalles al gráfico
plt.xlabel('Fecha')
plt.ylabel('Cotización')
plt.title('Evolución de las Cotizaciones de Dólar')
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.xticks(rotation=45)
plt.tight_layout()  # Ajustar el diseño para evitar el recorte de etiquetas
plt.show()
