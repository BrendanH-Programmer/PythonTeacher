let hintLevel = 1;

// --------------------
// AUTH
// --------------------
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
        document.getElementById("lessonCard").classList.remove("hidden");
        document.getElementById("tutorCard").classList.remove("hidden");
    }
}

// --------------------
// AI TUTOR (placeholder for now)
// --------------------
async function sendCode() {
    const code = document.getElementById("codeInput").value;

    const res = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code,
            hint_level: hintLevel
        })
    });

    const data = await res.json();

    document.getElementById("responseBox").innerText =
        data.hint || "No response";

    const table = document.getElementById("errorTable");
    table.innerHTML = "";

    if (data.errors) {
        data.errors.forEach(err => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${err.error_type}</td>
                <td>${err.priority}</td>
                <td>${err.message}</td>
            `;
            table.appendChild(row);
        });
    }
}

function nextHint() {
    hintLevel = Math.min(hintLevel + 1, 3);
    sendCode();
}