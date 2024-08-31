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
                    showLoginSuccessMessage();
                    // Redirigir a la nueva página
                    window.location.href = '/movimientos';  // Ajusta la URL según sea necesario
                } else {
                    document.getElementById('refreshAccessTokenResponse').innerText = 'Error: ' + data.error;
                    showLoginErrorMessage();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showLoginErrorMessage();
            });
    } else {
        document.getElementById('refreshAccessTokenResponse').innerText = 'No refresh token available.';
        showLoginErrorMessage();
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
            accounts.innerHTML = '<option value="">Seleccione una cuenta</option>';
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

function getAccountMovements() 
{
    const movementsErrormessage = document.getElementById('movementsErrormessage');
    const tbody = document.querySelector('#movimientos tbody');
    tbody.innerHTML = ''; // Limpiar tabla

    if (window.accessToken) 
    {
        fetch('/get_account_movements', 
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
                  'accounts': document.getElementById("accounts").value,
                  'date_from': document.getElementById("date_from").value,
                  'date_to': document.getElementById("date_to").value,
                  'ticker': document.getElementById("ticker").value,
                })
        })
        .then(response => response.json())
        .then(data => 
        {       
            if (data.error) 
            {
                movementsErrormessage.innerText = data.error; // Se coloca el mensaje de error obtenido
            } 
            else 
            {
                data.forEach(mov => {
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
        })
        .catch(error => console.error('Error:', error));
    } 
    else 
    {
        movementsErrormessage.innerText = 'No access token available.';
    }
}

// Otras funciones

function togglePasswordVisibility() 
{
    var passwordInput = document.getElementById('private_key');
    var eyeOpen = document.getElementById('eye-open');
    var eyeClosed = document.getElementById('eye-closed');

    if (passwordInput.type === 'password') 
    {
        passwordInput.type = 'text';
        eyeOpen.style.display = 'none';
        eyeClosed.style.display = 'inline';
    } 
    else 
    {
        passwordInput.type = 'password';
        eyeOpen.style.display = 'inline';
        eyeClosed.style.display = 'none';
    }
}

// Init layout
document.addEventListener("DOMContentLoaded", function() 
{
    // Se ocultan campos de mensajes
    var logInTokenResponse = document.getElementById("logInTokenResponse");
    if (logInTokenResponse) {
        logInTokenResponse.style.display = "none";
    }
    var refreshAccessTokenResponse = document.getElementById("refreshAccessTokenResponse");
    if (refreshAccessTokenResponse) {
        refreshAccessTokenResponse.style.display = "none";
    }
    var accountsErrormessage = document.getElementById("accountsErrormessage");
    if (accountsErrormessage) {
        accountsErrormessage.style.display = "none";
    }
    var movementsErrormessage = document.getElementById("movementsErrormessage");
    if (movementsErrormessage) {
        movementsErrormessage.style.display = "none";
    }
    var loginSuccessMessage = document.getElementById("loginSuccessMessage");
    if (loginSuccessMessage) {
        loginSuccessMessage.style.display = "none";
    }
    var loginErrorMessage = document.getElementById("loginErrorMessage");
    if (loginErrorMessage) {
        loginErrorMessage.style.display = "none";
    }
});

function showLoginSuccessMessage() 
{
    var successMessage = document.getElementById("loginSuccessMessage");
    if (successMessage) {
        successMessage.style.display = "block";
    }
}

function showLoginErrorMessage() 
{
    var successMessage = document.getElementById("loginErrorMessage");
    if (successMessage) {
        successMessage.style.display = "block";
    }
}

// Obtener Balance y posiciones

function ObtenerBalanceYposiciones() { //vinculo con HTML
    const movPosErrormessage = document.getElementById('movPosErrormessage');
    const availabilityTableBody = document.querySelector('#availabilityTable tbody');
    const instrumentsTableBody = document.querySelector('#instrumentsTable tbody');
    availabilityTableBody.innerHTML = ''; // Limpiar tabla
    instrumentsTableBody.innerHTML = ''; // Limpiar tabla

    if (window.accessToken) {
        fetch('/ObtenerBalanceYposiciones', { // Llama a la función de Python
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + window.accessToken
            },
            body: JSON.stringify({
                'ambiente_sand': document.getElementById("ambiente_sand").checked,
                'accounts': document.getElementById("accounts").value
            })
        })
        .then(response => response.json()) // Convierte la respuesta a JSON
        .then(data => {
            if (data.error) {
                movPosErrormessage.innerText = data.error; // Muestra el mensaje de error si ocurre
            } else {
                // Procesa y muestra los datos en las tablas
                data.groupedAvailability.forEach(group => {
                    group.availability.forEach(item => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${group.currency}</td>
                            <td>${item.name}</td>
                            <td>${item.symbol}</td>
                            <td>${item.amount.toFixed(2)}</td>
                            <td>${item.settlement}</td>
                        `;
                        availabilityTableBody.appendChild(row);
                    });
                });

                data.groupedInstruments.forEach(group => {
                    group.instruments.forEach(instrument => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${group.name}</td>
                            <td>${instrument.ticker}</td>
                            <td>${instrument.description}</td>
                            <td>${instrument.currency}</td>
                            <td>${instrument.price.toFixed(2)}</td>
                            <td>${instrument.amount.toFixed(2)}</td>
                        `;
                        instrumentsTableBody.appendChild(row);
                    });
                });
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        movPosErrormessage.innerText = 'No access token available.';
    }
}