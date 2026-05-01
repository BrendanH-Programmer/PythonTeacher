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
        // go to main app explicitly
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


// -------------------- SESSION CHECK (SAFE VERSION) --------------------
async function checkLogin() {
    try {
        const res = await fetch("http://127.0.0.1:5000/auth/me", {
            credentials: "include"
        });

        const data = await res.json();

        if (!data.logged_in) {
            window.location.href = "/login.html";
        } else {
            const userBox = document.getElementById("userInfo");
            if (userBox) {
                userBox.innerText = `Logged in as: ${data.user}`;
            }
        }
    } catch (err) {
        console.error("Session check failed:", err);
        window.location.href = "/login.html";
    }
}