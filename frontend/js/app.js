let hintLevel = 0;
let lastCode = "";
let currentLessonId = 1;

let lessonCompleted = false;
let hasAnalysed = false;
let isAnalyzing = false; // 🔥 CRITICAL FIX (prevents race conditions)


// -------------------------
// UI STATE CONTROLLER
// -------------------------
function syncHintButton() {

    const hintButton = document.getElementById("hintBtn");
    if (!hintButton) return;

    hintButton.disabled =
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

    // -------------------------
    // HARD GLOBAL LOCK
    // -------------------------
    if (isAnalyzing) return;

    // -------------------------
    // RESET STATE IF CODE CHANGES
    // -------------------------
    if (code !== lastCode && !getHint) {

        hintLevel = 0;
        lessonCompleted = false;
        hasAnalysed = false;

        lastCode = code;

        updateHintUI();
        syncHintButton();
    }

    // -------------------------
    // HANDLE HINT REQUEST (FULL SAFETY LOCK)
    // -------------------------
    if (getHint) {

        if (isAnalyzing || lessonCompleted || !hasAnalysed || hintLevel >= 3) {
            return;
        }

        hintLevel++;
        updateHintUI();
        syncHintButton();
    }

    // -------------------------
    // START ANALYSIS LOCK
    // -------------------------
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
                lesson_id: currentLessonId
            })
        });

        const data = await res.json();

        // -------------------------
        // SERVER ERROR
        // -------------------------
        if (data.success === false) {
            responseBox.innerText = "❌ Server error.";
            return;
        }

        // -------------------------
        // CORRECT ANSWER (FULL LOCK)
        // -------------------------
        if (data.correct) {

            lessonCompleted = true;
            hasAnalysed = true;
            hintLevel = 0;

            responseBox.innerText =
                `✅ Well done Brendan!\n\n${data.message}\n\n🎯 Lesson task completed.\n\nYou can still use hints to explore improvements or deeper understanding.`;

            updateHintUI();
            syncHintButton();

            return;
        }

        // -------------------------
        // INCORRECT ANSWER
        // -------------------------
        hasAnalysed = true;

        responseBox.innerText = `${data.message}`;

        syncHintButton();

    } finally {

        // -------------------------
        // ALWAYS RELEASE LOCK
        // -------------------------
        isAnalyzing = false;
        syncHintButton();
    }
}


// -------------------------
// NEXT HINT BUTTON
// -------------------------
function nextHint() {

    // HARD SAFETY GATES
    if (isAnalyzing) return;
    if (lessonCompleted) return;
    if (!hasAnalysed) return;
    if (hintLevel >= 3) return;

    sendCode(true);
}