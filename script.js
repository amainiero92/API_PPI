async function conectarApi() {
    const url = "https://clientapi_sandbox.portfoliopersonal.com/api/1.0/Account/LoginApi";

    const headers = {
        "AuthorizedClient": "API_CLI_REST",
        "ClientKey": "ppApiCliSB",
        "Content-Type": "application/json",
        "ApiKey": "VHltelE1SG5EOGZrdndzdE5ZMU4=",
        "ApiSecret": "MjA3MDBhNzItNmMzOC00YzRhLWIyMzQtOGUwNGYyODY3ZWY0"
    };

    try {
        const response = await fetch(url, {
            method: 'POST', // Cambiar a 'GET' si es necesario
            headers: headers,
            body: JSON.stringify({ /* datos que necesites enviar */ }) // Cambia aquí si necesitas enviar datos
        });

        if (!response.ok) {
            throw new Error('Error en la red');
        }

        const data = await response.json();
        document.getElementById('result').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerText = 'Error: ' + error.message;
    }
}

