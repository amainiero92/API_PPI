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

function fetchAccounts() {
    if (window.accessToken) {
        fetch('/get_accounts', {
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
                if (data.error) {
                    document.getElementById('accounts').innerText = 'Error: ' + data.error;
                } else {
                    document.getElementById('accounts').innerText = 'Accounts: ' + JSON.stringify(data, null, 2);
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('accounts').innerText = 'No access token available.';
    }
}