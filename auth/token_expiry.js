function checkAndRemoveExpiredToken() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        // No token found, no action needed
        return;
    }

    // Decode the JWT token to get the payload
    const payloadBase64Url = token.split('.')[1];
    const payloadBase64 = payloadBase64Url.replace('-', '+').replace('_', '/');
    const payload = JSON.parse(window.atob(payloadBase64));

    // Check if the token has expired
    const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds
    if (payload.exp < currentTime) {
        // Token has expired, remove it from local storage
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_info')


        // Optionally, prompt the user to log in again
        const userConfirmation = window.confirm("Your session has expired. Please log in again.");
        if (userConfirmation) {
            window.location.href = 'login.html'; // Redirect to login page
        }
    }
}

// Call this function at appropriate times, such as on page load or before making API requests
checkAndRemoveExpiredToken();
