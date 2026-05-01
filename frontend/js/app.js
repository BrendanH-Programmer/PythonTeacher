let hintLevel = 1;

async function sendCode(reset = true) {
    const code = document.getElementById("codeInput").value;
    const responseBox = document.getElementById("responseBox");
    const tableBody = document.getElementById("errorTable");

    if (reset) hintLevel = 1;

    responseBox.innerText = "Running analysis...";

    try {
        const res = await fetch("http://127.0.0.1:5000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({
                code,
                hint_level: hintLevel
            })
        });

        const data = await res.json();

        // -------------------
        // HINT OUTPUT
        // -------------------
        responseBox.innerText =
            `Hint Level ${hintLevel}:\n\n` +
            (data.hint || "No hint returned");

        // -------------------
        // ERROR TABLE
        // -------------------
        tableBody.innerHTML = "";

        if (data.errors && data.errors.length > 0) {

            data.errors.forEach(err => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${err.error_type || "Unknown"}</td>
                    <td>${err.priority ?? "-"}</td>
                    <td>${err.message || "No message"}</td>
                `;

                tableBody.appendChild(row);
            });

        } else {
            tableBody.innerHTML =
                "<tr><td colspan='3'>No errors detected</td></tr>";
        }

    } catch (error) {
        console.error(error);
        responseBox.innerText = "Error connecting to server.";
    }
}

function nextHint() {
    hintLevel = Math.min(hintLevel + 1, 3);
    sendCode(false);
}