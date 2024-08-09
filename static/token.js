function fetchRefreshToken() {
    fetch('/get_refresh_token')
        .then(response => response.json())
        .then(data => {
            if (data.refreshToken) {
                document.getElementById('response').innerText = 'Refresh Token: ' + data.refreshToken;
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

function fetchAccounts() {
    if (window.accessToken) {
        fetch('/get_accounts')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('response').innerText = 'Error: ' + data.error;
                } else {
                    document.getElementById('response').innerText = 'Accounts: ' + JSON.stringify(data, null, 2);
                }
            })
            .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('response').innerText = 'No access token available.';
    }
}
