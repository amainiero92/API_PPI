from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Función para hacer scraping y obtener el valor debajo de "Fin de Mes Compra"
def obtener_fin_mes_compra(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    app.logger.info(soup)

    # Encontrar el div que contiene "Fin de Mes Compra"
    elemento = soup.find('div', string='Compra')

    if elemento:
        # Buscar el siguiente div que contiene el número
        valor_div = elemento.find_next('div', class_='h5 mb-0 font-weight-bold text-gray-800')
        if valor_div:
            return valor_div.text.strip()
        else:
            return "Valor no encontrado"
    else:
        return "Texto 'Fin de Mes Compra' no encontrado"

@app.route('/', methods=['GET', 'POST'])
def index():
    valor = None
    if request.method == 'POST':
        mes = request.form['mes']
        url = f'https://dolarhistorico.com/dolar-blue/cotizacion/{mes}'
        valor = obtener_fin_mes_compra(url)

    return render_template('dolar.html', valor=valor)

if __name__ == '__main__':
    app.run(debug=True)