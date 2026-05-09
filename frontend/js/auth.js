// -------------------- 
// AUTHENTICATION FUNCTIONS
// These functions handle user authentication, including login, registration, logout, and session checking. They interact with the backend API to manage user sessions and update the UI accordingly based on the user's authentication status.
// --------------------

// --------------------
// LOGIN
// This function handles the user login process by sending the username to the backend API, receiving a response, and updating the UI based on the success of the login attempt. If the login is successful, it redirects the user to the main page; otherwise, it displays an error message.
// --------------------
async function login() {

    // Get the username from the input field
    const username = document.getElementById("username").value;

    // Send a POST request to the login endpoint with the username
    const res = await fetch("http://127.0.0.1:5000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username })
    });

    // Parse the JSON response from the server
    const data = await res.json();

    // Update the authentication status message in the UI based on the response from the server
    const status = document.getElementById("authStatus");
    if (status) status.innerText = data.message;

    // If the login was successful, redirect the user to the main page
    if (data.success) {
        window.location.href = "/index.html";
    }
}

// --------------------
// REGISTER
// This function handles the user registration process by sending the username to the backend API, receiving a response, and updating the UI based on the success of the registration attempt. It provides feedback to the user about the registration status.
// --------------------
async function register() {

    // Get the username from the input field
    const username = document.getElementById("username").value;

    // Send a POST request to the registration endpoint with the username
    const res = await fetch("http://127.0.0.1:5000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })
    });

    // Parse the JSON response from the server
    const data = await res.json();

    // Update the authentication status message in the UI based on the response from the server
    const status = document.getElementById("authStatus");
    if (status) status.innerText = data.message;
}


// -------------------- 
// LOGOUT
// This function handles the user logout process by sending a POST request to the logout endpoint of the backend API, and then redirecting the user to the login page. It ensures that the user's session is properly terminated on the server side before redirecting.
// --------------------
async function logout() {

    // Send a POST request to the logout endpoint to terminate the user's session
    await fetch("http://127.0.0.1:5000/auth/logout", {
        method: "POST",
        credentials: "include"
    });

    // Redirect the user to the login page after logging out
    window.location.href = "/login.html";
}


// --------------------
// CHECK LOGIN STATUS
// This function checks if the user is currently logged in by sending a request to the backend API, and updates the UI accordingly. If the user is not logged in, it redirects them to the login page. If they are logged in, it displays their username in the UI.
// --------------------
async function checkLogin() {

    // Send a request to the backend API to check the user's login status
    try {
        const res = await fetch("http://127.0.0.1:5000/auth/me", {
            credentials: "include"
        });

        // Parse the JSON response from the server
        const data = await res.json();

        // If the user is not logged in, redirect them to the login page
        if (!data.logged_in) {
            window.location.href = "/login.html";
            return;
        }

        // If the user is logged in, update the UI to display their username
        const userBox = document.getElementById("userInfo");
        if (userBox) {
            userBox.innerText = `Logged in as: ${data.user}`;
        }

        // Return the user data for further use in the application
    } catch (err) {
        window.location.href = "/login.html";
    }
}