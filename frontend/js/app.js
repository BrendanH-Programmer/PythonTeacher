let hintLevel = 1;

// -------------------------
// MAIN AI ANALYSIS
// -------------------------
async function sendCode() {

    const code = document.getElementById("codeInput").value;
    const responseBox = document.getElementById("responseBox");
    const tableBody = document.getElementById("errorTable");

    if (!code.trim()) {
        responseBox.innerText = "⚠️ Please enter some code first.";
        return;
    }

    responseBox.innerText = "⏳ Analysing...";

    try {
        const res = await fetch("http://127.0.0.1:5000/api/ai/analyse", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({ code })
        });

        const data = await res.json();

        if (!data.success) {
            responseBox.innerText = "❌ Error analysing code.";
            return;
        }

        // -------------------------
        // OUTPUT (AI)
        // -------------------------
        responseBox.innerText =
            "🧠 Feedback:\n\n" +
            data.feedback +
            "\n\n💡 Suggestion:\n" +
            data.suggestion;

        // -------------------------
        // OPTIONAL ERROR TABLE RESET
        // -------------------------
        if (tableBody) {
            tableBody.innerHTML =
                "<tr><td colspan='3'>AI analysis complete</td></tr>";
        }

    } catch (error) {
        console.error(error);
        responseBox.innerText = "❌ Server error.";
    }
}


// -------------------------
// OPTIONAL: NEXT HINT (extend later)
// -------------------------
function nextHint() {
    hintLevel = Math.min(hintLevel + 1, 3);
    sendCode();
}


// -------------------------
// NAVIGATION
// -------------------------
function updateNavButtons() {
    const nextBtn = document.getElementById("nextBtn");
    const finishBtn = document.getElementById("finishBtn");

    // Add logic later
}