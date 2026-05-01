let currentLesson = 1;
let currentSectionIndex = 0;

const sectionsOrder = [
    "intro",
    "outcomes",
    "demo",
    "practice",
    "review"
];

async function startLesson() {
    currentLesson = document.getElementById("lessonSelect").value;
    currentSectionIndex = 0;
    loadSection();
}

async function loadSection() {

    const section = sectionsOrder[currentSectionIndex];

    const res = await fetch(
        `http://127.0.0.1:5000/api/lesson/${currentLesson}/section/${section}`,
        { credentials: "include" }
    );

    const data = await res.json();

    currentLesson = parseInt(document.getElementById("lessonSelect").value);
    const title = document.getElementById("lessonTitle");

    title.innerText = data.lesson_title + " - " + section.toUpperCase();

    const content = data.data;

    // ---------------- INTRO ----------------
    if (section === "intro") {
        box.innerHTML = `<p>${content.content}</p>`;
    }

    // ---------------- OUTCOMES ----------------
    if (section === "outcomes") {

        box.innerHTML = `
            <h3>Learning Outcomes</h3>
            <ul>
                ${content.content.map(o => `<li>${o}</li>`).join("")}
            </ul>
        `;
    }

    // ---------------- DEMO ----------------
    if (section === "demo") {

        box.innerHTML = `
            <h3>Demo Code</h3>
            <pre>${content.code}</pre>
            <p>${content.explanation}</p>
        `;
    }

    // ---------------- PRACTICE ----------------
    if (section === "practice") {

        document.getElementById("tutorCard").classList.remove("hidden");

        box.innerHTML = `
            <h3>Practice Task</h3>
            <p>${content.task}</p>
            <p><b>Use the AI tutor below to help you.</b></p>
        `;
    }

    // ---------------- REVIEW ----------------
    if (section === "review") {

        document.getElementById("tutorCard").classList.add("hidden");

        box.innerHTML = `
            <h3>Review</h3>
            <p>${content.summary}</p>
            <p>Great work! You can now move to the next lesson.</p>
        `;
    }
}

function nextSection() {

    if (currentSectionIndex < sectionsOrder.length - 1) {
        currentSectionIndex++;
        loadSection();
    }
}

function prevSection() {

    if (currentSectionIndex > 0) {
        currentSectionIndex--;
        loadSection();
    }
}