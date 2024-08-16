function logIn() {
    fetch('/LoginApi', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            { 
                'public_key': document.getElementById("public_key").value,
                'private_key': document.getElementById("private_key").value,
                'ambiente_sand': document.getElementById("ambiente_sand").checked,
            })
    })
        .then(response => response.json()) // Convierte la respuesta a JSON
        .then(data => { // Utiliza los datos JSON
            if (data.refreshToken) {
                document.getElementById('logInTokenResponse').innerText = 'Refresh Token: ' + data.refreshToken;
                window.refreshToken = data.refreshToken;
                refreshAccessToken();
            } else {
                document.getElementById('logInTokenResponse').innerText = 'Error: ' + data.error;
            }
        })
        .catch(error => console.error('Error:', error));
}

function refreshAccessToken() {
    if (window.refreshToken) {
        fetch('/refresh_access_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + window.refreshToken
            },
            body: JSON.stringify(
                { 
                  'refreshToken': window.refreshToken,
                  'ambiente_sand': document.getElementById("ambiente_sand").checked,  
                })
        })
            .then(response => response.json())
            .then(data => {
                if (data.accessToken) {
                    window.accessToken = data.accessToken;
                    document.getElementById('refreshAccessTokenResponse').innerText = 'Access Token: ' + data.accessToken;
                } else {
                    document.getElementById('refreshAccessTokenResponse').innerText = 'Error: ' + data.error;
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('refreshAccessTokenResponse').innerText = 'No refresh token available.';
    }
}

function fetchAccounts() 
{
    const accounts = document.getElementById('accounts');
    const accountsErrormessage = document.getElementById('accountsErrormessage');

    if (window.accessToken) 
    {
        fetch('/get_accounts', 
        {
            method: 'POST',
            headers: 
            {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + window.refreshToken
            },
            body: JSON.stringify(
                { 
                  'refreshToken': window.refreshToken,
                  'ambiente_sand': document.getElementById("ambiente_sand").checked,  
                })
        })
        .then(response => response.json())
        .then(data => 
        {       
            accounts.innerHTML = ''; // Se limpia los valores del campo lista antes de comenzar
            accounts.innerHTML = '<option value="">Seleccione una opción</option>';
            if (data.error) 
            {
                accountsErrormessage.innerText = data.error; // Se coloca el mensaje de error obtenido
            } 
            else 
            {
                data.forEach(result => {
                    const newAccount = document.createElement('option');
                    newAccount.value = result.accountNumber;
                    newAccount.textContent = result.name;
                    accounts.appendChild(newAccount);
                });
            }
        })
        .catch(error => console.error('Error:', error));
    } 
    else 
    {
        accountsErrormessage.innerText = 'No access token available.';
    }
}

function getAccountMovements() {
    // Llamada a la API para buscar movimientos
    // Reemplaza con la lógica para llamar a la API
    const movimientos = [
        {
            agreementDate: '2024-08-01',
            settlementDate: '2024-08-02',
            moneda: 'USD',
            amount: 1000.00,
            price: 100.50,
            description: 'Compra de acciones',
            ticker: 'AAPL',
            quantity: 10,
            balance: 1000.00
        },
        // Más movimientos...
    ];

    const tbody = document.querySelector('#movimientos tbody');
    tbody.innerHTML = ''; // Limpiar tabla

    movimientos.forEach(mov => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${mov.agreementDate}</td>
            <td>${mov.settlementDate}</td>
            <td>${mov.moneda}</td>
            <td>${mov.amount.toFixed(2)}</td>
            <td>${mov.price.toFixed(2)}</td>
            <td>${mov.description}</td>
            <td>${mov.ticker}</td>
            <td>${mov.quantity.toFixed(2)}</td>
            <td>${mov.balance.toFixed(2)}</td>
        `;
        tbody.appendChild(row);
    });
}