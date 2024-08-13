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
                'ambiente_sand': document.getElementById("ambiente_sand").value,
            })
    })
        .then(response => response.json()) // Convierte la respuesta a JSON
        .then(data => { // Utiliza los datos JSON
            if (data.refreshToken) {
                document.getElementById('response').innerText = 'Refresh Token: ' + data.refreshToken;
                window.refreshToken = data.refreshToken;
                refreshAccessToken();
            } else {
                document.getElementById('response').innerText = 'Error: ' + data.error;
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
            body: JSON.stringify({ 'refreshToken': window.refreshToken })
        })
            .then(response => response.json())
            .then(data => {
                if (data.accessToken) {
                    window.accessToken = data.accessToken;
                    document.getElementById('response').innerText = 'Access Token: ' + data.accessToken;
                } else {
                    document.getElementById('response').innerText = 'Error: ' + data.error;
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('response').innerText = 'No refresh token available.';
    }
}