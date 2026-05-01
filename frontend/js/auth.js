// -------------------- LOGIN --------------------
async function login() {
    const username = document.getElementById("username").value;

    const res = await fetch("http://127.0.0.1:5000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ username })
    });

    const data = await res.json();

    document.getElementById("authStatus").innerText = data.message;

    if (data.success) {
        window.location.href = "/index.html";
    }
}


// -------------------- REGISTER --------------------
async function register() {
    const username = document.getElementById("username").value;

    const res = await fetch("http://127.0.0.1:5000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username })
    });

    const data = await res.json();

    document.getElementById("authStatus").innerText = data.message;
}


// -------------------- LOGOUT --------------------
async function logout() {
    await fetch("http://127.0.0.1:5000/auth/logout", {
        method: "POST",
        credentials: "include"
    });

    window.location.href = "/login.html";
}


// -------------------- SESSION GUARD (IMPORTANT) --------------------
async function checkLogin() {
    const res = await fetch("http://127.0.0.1:5000/auth/me", {
        credentials: "include"
    });

    const data = await res.json();

    if (!data.logged_in) {
        window.location.href = "/login.html";
    }
}