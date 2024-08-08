function fetchRefreshToken() {
    fetch('/get_refresh_token')
        .then(response => response.json())
        .then(data => {
            if (data.refreshToken) {
                document.getElementById('response').innerText = 'Refresh Token: ' + data.refreshToken;
                // Guardar el refreshToken en una variable global de JavaScript
                window.refreshToken = data.refreshToken;
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
                document.getElementById('response').innerText = 'Response: ' + JSON.stringify(data);
            })
            .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('response').innerText = 'No refresh token available.';
    }
}