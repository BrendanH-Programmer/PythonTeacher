let hintLevel = 0;
let lastCode = "";

async function sendCode(getHint = false) {

    const code = document.getElementById("codeInput").value;
    const responseBox = document.getElementById("responseBox");
    const hintButton = document.getElementById("hintBtn");

    if (!code.trim()) {
        responseBox.innerText = "⚠️ Please enter some code first.";
        return;
    }

    if (code !== lastCode) {
        hintLevel = 0;
        lastCode = code;

        // reset hint button when code changes
        if (hintButton) hintButton.disabled = false;
    }

    if (getHint) {
        hintLevel = Math.min(hintLevel + 1, 3);
    }

       // LOCK HINTS AT MAX LEVEL
    if (hintLevel >= 3 && hintButton) {
        hintButton.disabled = true;
    }

    responseBox.innerText = "⏳ Analysing...";

    const res = await fetch("http://127.0.0.1:5000/api/ai/analyse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
            code,
            hint_level: hintLevel
        })
    });

    const data = await res.json();

    if (!data.success) {
        responseBox.innerText = "❌ Server error.";
        return;
    }

    // -------------------------
    // CORRECT
    // -------------------------
    if (data.correct === true) {

        responseBox.innerText =
            `✅ Well done Brendan!\n\n${data.message}\n\nClick Hint for extra improvement tips!`;

        hintLevel = 0;
        return;
    }

    // -------------------------
    // INCORRECT (AI RESPONSE ONLY)
    // -------------------------
    responseBox.innerText =
        `❌ ${data.message}`;
}

function nextHint() {
    sendCode(true);
}