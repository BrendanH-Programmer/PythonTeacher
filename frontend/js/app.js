let hintLevel = 0;
let lastCode = "";

let lessonCompleted = false;
let hasAnalysed = false;
let isAnalyzing = false;

// -------------------------
// UI STATE CONTROLLER
// -------------------------
function syncHintButton() {

    const hintButton = document.getElementById("hintBtn");
    if (!hintButton) return;

    hintButton.disabled =
        lessonCompleted ||
        !hasAnalysed ||
        hintLevel >= 3 ||
        isAnalyzing;
}

// -------------------------
// HINT UI TEXT
// -------------------------
function updateHintUI() {

    const hintInfo = document.getElementById("hintInfo");
    if (!hintInfo) return;

    hintInfo.innerText =
        hintLevel === 0 ? "" : `Hint ${hintLevel}/3 used`;
}

// -------------------------
// MAIN ANALYSIS FUNCTION
// -------------------------
async function sendCode(getHint = false) {
    const code = document.getElementById("codeInput").value.trim();
    const responseBox = document.getElementById("responseBox");

    if (!code) {
        responseBox.innerText = "⚠️ Please enter some code first.";
        return;
    }

    const lessonId = window.currentLessonId; // 🔥 FIXED SAFE ACCESS

    if (!lessonId) {
        responseBox.innerText = "❌ Lesson not initialised.";
        return;
    }

    if (isAnalyzing) return;

    // reset on new code
    if (code !== lastCode && !getHint) {

        hintLevel = 0;
        lessonCompleted = false;
        hasAnalysed = false;

        lastCode = code;

        updateHintUI();
        syncHintButton();
    }

    if (getHint) {

        if (lessonCompleted || !hasAnalysed || hintLevel >= 3) {
            return;
        }

        hintLevel++;
        updateHintUI();
    }

    isAnalyzing = true;
    responseBox.innerText = "⏳ Analysing...";
    syncHintButton();

    try {

        const res = await fetch("http://127.0.0.1:5000/api/ai/analyse", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({
                code,
                hint_level: hintLevel,
                lesson_id: lessonId
            })
        });

        const data = await res.json();

        if (!data.success) {
            responseBox.innerText = "❌ Server error.";
            return;
        }

        hasAnalysed = true;

        // -------------------------
        // CORRECT
        // -------------------------
        if (data.correct) {

            lessonCompleted = true;
            hintLevel = 0;

            responseBox.innerText =
                `✅ Well done Brendan!\n\n${data.message}\n\n🎯 Lesson complete.`;

            updateHintUI();
            syncHintButton();

            return;
        }

        // -------------------------
        // INCORRECT
        // -------------------------
        responseBox.innerText = data.message;

        syncHintButton();

    } finally {
        isAnalyzing = false;
        syncHintButton();
    }
}

// -------------------------
function nextHint() {
    if (isAnalyzing) return;
    if (lessonCompleted) return;
    if (!hasAnalysed) return;
    if (hintLevel >= 3) return;

    sendCode(true);
}