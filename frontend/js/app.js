// -------------------------
// STATE VARIABLES
// -------------------------
let hintLevel = 0;
let lastCode = "";

let lessonCompleted = false;
let hasAnalysed = false;
let isAnalyzing = false;

// -------------------------
// UI STATE CONTROLLER
// This function manages the state of the hint button based on various conditions such as whether the lesson is completed, if the user has analysed their code, if they've used all available hints, or if an analysis is currently in progress, by enabling or disabling the hint button accordingly, it provides a better user experience by preventing actions that are not allowed in the current state of the lesson and guiding the user through the learning process
// -------------------------
function syncHintButton() {

    // Disable the hint button if the lesson is completed, if the user hasn't analysed their code yet, if they've used all hints, or if an analysis is currently in progress
    const hintButton = document.getElementById("hintBtn");
    if (!hintButton) return;

    // The hint button is disabled if the lesson is completed, if the user hasn't analysed their code yet, if they've used all hints, or if an analysis is currently in progress
    hintButton.disabled =
        lessonCompleted ||
        !hasAnalysed ||
        hintLevel >= 3 ||
        isAnalyzing;
}

// -------------------------
// HINT UI TEXT
// Updates the hint information text based on the current hint level, if no hints have been used, it clears the text, otherwise it displays how many hints have been used out of the total available (3 in this case), this provides feedback to the user about their hint usage and encourages them to try solving the problem on their own before using hints
// -------------------------
function updateHintUI() {

    // Update the hint information text to show how many hints have been used, or clear it if no hints have been used
    const hintInfo = document.getElementById("hintInfo");
    if (!hintInfo) return;

    // If no hints have been used, clear the hint information text, otherwise show how many hints have been used out of 3
    hintInfo.innerText =
        hintLevel === 0 ? "" : `Hint ${hintLevel}/3 used`;
}

// -------------------------
// MAIN ANALYSIS FUNCTION
// -------------------------
async function sendCode(getHint = false) {

    // Get the code from the input field and the response box element
    const code = document.getElementById("codeInput").value.trim();
    const responseBox = document.getElementById("responseBox");

    // If the code input is empty, show a warning message and return early to prevent sending an empty request to the server
    if (!code) {
        responseBox.innerText = "⚠️ Please enter some code first.";
        return;
    }

    // Safely access the current lesson ID from the global window object, if it's not available, show an error message and return early to prevent sending a request without a valid lesson ID, this ensures that the function has all the necessary information to perform the analysis and provides feedback to the user if something is missing
    const lessonId = window.currentLessonId; // 🔥 FIXED SAFE ACCESS

    // If the lesson ID is not available, show an error message and return early to prevent sending a request without a valid lesson ID
    if (!lessonId) {
        responseBox.innerText = "❌ Lesson not initialised.";
        return;
    }

    // If an analysis is currently in progress, return early to prevent multiple simultaneous analyses, this helps to manage the state of the application and ensures that the user doesn't accidentally trigger multiple requests to the server while waiting for a response
    if (isAnalyzing) return;

    // reset on new code
    if (code !== lastCode && !getHint) {

        hintLevel = 0;
        lessonCompleted = false;
        hasAnalysed = false;

        lastCode = code;

        // Update the hint information text and sync the hint button state when the user enters new code, this ensures that the UI reflects the reset state of the lesson when the user starts working on a new solution, providing a clear indication that they can start fresh with their analysis and hint usage
        updateHintUI();
        syncHintButton();
    }

    if (getHint) {

        // If the user is requesting a hint, check if the lesson is already completed, if they haven't analysed their code yet, or if they've used all available hints, and return early if any of those conditions are true to prevent providing hints when they are not applicable, this encourages the user to engage with the problem-solving process and use hints strategically
        if (lessonCompleted || !hasAnalysed || hintLevel >= 3) {
            return;
        }

        // If the user is requesting a hint and it's allowed, increment the hint level to provide the next hint, this allows the user to receive additional guidance on their solution while still encouraging them to try solving the problem on their own before using too many hints
        hintLevel++;
        updateHintUI();
    }

    // Set the analyzing state to true and update the response box to indicate that the analysis is in progress, this provides feedback to the user that their code is being processed and helps manage the state of the application to prevent multiple analyses from being triggered simultaneously
    isAnalyzing = true;
    responseBox.innerText = "⏳ Analysing...";
    syncHintButton();

    try {

        // Send the code, hint level, and lesson ID to the server for analysis, this allows the backend to evaluate the user's code against the lesson requirements and provide feedback, hints, or a success message based on the correctness of the solution and the current hint level
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

        // Parse the JSON response from the server, this will contain information about whether the user's code is correct, any feedback or hints, and whether the analysis was successful, this data is used to update the UI and guide the user through the learning process based on their solution
        const data = await res.json();

        // If the analysis was not successful, show an error message in the response box and return early to prevent further processing, this provides feedback to the user that something went wrong with the analysis and encourages them to try again or check their code for issues
        if (!data.success) {
            responseBox.innerText = "❌ Server error.";
            return;
        }

        // Mark that the user has analysed their code at least once, this allows the application to enable the hint button and provide hints if the user's initial solution is not correct, encouraging them to engage with the problem-solving process and use hints strategically
        hasAnalysed = true;

        // -------------------------
        // CORRECT
        // If the user's code is correct, mark the lesson as completed, reset the hint level, and update the response box with a success message and any additional feedback from the server, this provides positive reinforcement to the user for solving the problem correctly and indicates that they have completed the lesson, while also encouraging them to review any feedback provided by the server to understand their solution better
        // -------------------------
        if (data.correct) {

            lessonCompleted = true;
            hintLevel = 0;

            // Update the response box with a success message and any additional feedback from the server, this provides positive reinforcement to the user for solving the problem correctly and indicates that they have completed the lesson, while also encouraging them to review any feedback provided by the server to understand their solution better
            responseBox.innerText =
                `✅ Well done Brendan!\n\n${data.message}\n\n🎯 Lesson complete.`;

                // Update the hint information text and sync the hint button state when the lesson is completed, this ensures that the UI reflects the completed state of the lesson and prevents the user from requesting hints after they've successfully solved the problem
            updateHintUI();
            syncHintButton();

            return;
        }

        // -------------------------
        // INCORRECT
        // If the user's code is incorrect, update the response box with feedback from the server, this provides constructive feedback to the user about what might be wrong with their solution and encourages them to try again or use hints to improve their code, while still allowing them to engage with the problem-solving process and learn from their mistakes
        // -------------------------
        responseBox.innerText = data.message;

        // Sync the hint button state after receiving feedback from the server, this ensures that the UI reflects the current state of the lesson and allows the user to request hints if they haven't used all available hints yet, providing guidance as they work towards a correct solution
        syncHintButton();

        // If the user has used all available hints, provide additional encouragement in the response box to motivate them to keep trying, this helps to maintain a positive learning experience and encourages persistence in problem-solving even when the solution is not immediately apparent
    } finally {
        isAnalyzing = false;
        syncHintButton();
    }
}

// -------------------------
// NEXT HINT
// This function allows the user to request the next hint for their current solution, it checks if the user is currently analyzing their code, if the lesson is already completed, if they haven't analysed their code yet, or if they've used all available hints, and only sends a request for the next hint if none of those conditions are true, this encourages the user to engage with the problem-solving process and use hints strategically while providing guidance when needed
// -------------------------
function nextHint() {
    if (isAnalyzing) return;
    if (lessonCompleted) return;
    if (!hasAnalysed) return;
    if (hintLevel >= 3) return;

    sendCode(true);
}