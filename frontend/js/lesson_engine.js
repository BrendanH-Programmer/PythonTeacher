let currentLesson = 1;
let currentSectionIndex = 0;

let lessonProgress = {}; // per-lesson progress map

const sectionsOrder = [
    "intro",
    "outcomes",
    "demo",
    "practice",
    "review"
];


// -------------------------
// INIT LESSON
// -------------------------
async function initLessonFromURL() {

    await checkLogin();

    const params = new URLSearchParams(window.location.search);
    const id = Number(params.get("id"));

    if (!id) {
        window.location.href = "/index.html";
        return;
    }

    // -------------------------
    // GET LESSON ACCESS
    // -------------------------
    const res = await fetch("http://127.0.0.1:5000/api/user/lesson-status", {
        credentials: "include"
    });

    const data = await res.json();

    const lesson = data.lessons.find(l => l.id === id);

    if (!lesson || !lesson.unlocked) {
        alert("🔒 Lesson locked");
        window.location.href = "/index.html";
        return;
    }

    currentLesson = id;
    currentSectionIndex = 0;

    // -------------------------
    // LOAD PROGRESS (SAFE)
    // -------------------------
    const progressRes = await fetch("http://127.0.0.1:5000/api/user/progress", {
        credentials: "include"
    });

    const progressData = await progressRes.json();

    lessonProgress = Object.fromEntries(
        Object.entries(progressData.progress?.lessons || {})
            .map(([k, v]) => [String(k), v])
    );

    await loadSection();
}


// -------------------------
// LOAD SECTION
// -------------------------
async function loadSection() {

    const section = sectionsOrder[currentSectionIndex];

    const res = await fetch(
        `http://127.0.0.1:5000/api/lesson/${currentLesson}/section/${section}`,
        { credentials: "include" }
    );

    const data = await res.json();

    const box = document.getElementById("lessonContent");
    const title = document.getElementById("lessonTitle");
    const tutor = document.getElementById("tutorCard");
    const nav = document.querySelector(".row");

    title.innerText = `${data.lesson_title} - ${section.toUpperCase()}`;

    const content = data.data;

    if (nav) nav.style.display = "flex";
    tutor.classList.add("hidden");

    // -------------------------
    // INTRO + RESUME (FIXED)
    // -------------------------
    if (section === "intro") {

        const savedSection = lessonProgress[String(currentLesson)];

        let resumeUI = "";

        if (savedSection && savedSection !== "intro") {

            resumeUI = `
                <div class="resume-box">
                    <p>You previously reached: <strong>${savedSection.toUpperCase()}</strong></p>
                    <button onclick="jumpToSection('${savedSection}')">
                        Jump to where I left off
                    </button>
                </div>
            `;
        }

        box.innerHTML = `
            ${resumeUI}
            <p>${content.content}</p>
        `;
    }

    // -------------------------
    // OUTCOMES
    // -------------------------
    if (section === "outcomes") {
        box.innerHTML = `
            <ul>
                ${content.content.map(o => `<li>${o}</li>`).join("")}
            </ul>
        `;
    }

    // -------------------------
    // DEMO
    // -------------------------
    if (section === "demo") {
        box.innerHTML = `
            <pre>${content.code}</pre>
            <p>${content.explanation}</p>
        `;
    }

    // -------------------------
    // PRACTICE
    // -------------------------
    if (section === "practice") {
        tutor.classList.remove("hidden");
        box.innerHTML = `<p>${content.task}</p>`;
    }

    // -------------------------
    // REVIEW
    // -------------------------
    if (section === "review") {

        if (nav) nav.style.display = "none";

        box.innerHTML = `
            <p>${content.summary}</p>
            <h3>Lesson Complete ✓</h3>
            <button onclick="finishLesson()">Finish Lesson</button>
        `;
    }
    updateNavButtons();
}


// -------------------------
// SAVE PROGRESS
// -------------------------
async function markProgress() {

    const section = sectionsOrder[currentSectionIndex];

    await fetch("http://127.0.0.1:5000/api/lesson/progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
            lesson_id: currentLesson,
            section
        })
    });

    lessonProgress[String(currentLesson)] = section;
}


// -------------------------
// NEXT SECTION
// -------------------------
async function nextSection() {

    await markProgress();

    if (currentSectionIndex < sectionsOrder.length - 1) {
        currentSectionIndex++;
        await loadSection();
    }
}


// -------------------------
// FINISH LESSON
// -------------------------
async function finishLesson() {

    await fetch("http://127.0.0.1:5000/api/lesson/progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
            lesson_id: currentLesson,
            section: "review"
        })
    });

    window.location.href = "/index.html";
}


// -------------------------
// EXIT LESSON (IMPORTANT FIX)
// -------------------------
async function exitLesson() {

    await markProgress(); // ensures backend is updated first
    window.location.href = "/index.html";
}


// -------------------------
// JUMP TO SECTION
// -------------------------
function jumpToSection(sectionName) {

    const idx = sectionsOrder.indexOf(sectionName);

    if (idx !== -1) {
        currentSectionIndex = idx;
        loadSection();
    }
}

// -------------------------
// PREVIOUS SECTION
// -------------------------
async function prevSection() {

    if (currentSectionIndex <= 0) return;

    currentSectionIndex--;
    await loadSection();
}

// -------------------------
// UPDATE NAV BUTTON VISIBILITY
// -------------------------
function updateNavButtons() {

    const backBtn = document.querySelector(".row button:nth-child(1)");
    const nextBtn = document.querySelector(".row button:nth-child(2)");

    // Hide Back on first section
    if (currentSectionIndex === 0) {
        backBtn.style.display = "none";
    } else {
        backBtn.style.display = "inline-block";
    }

    // Hide Next on last section (optional but recommended)
    if (currentSectionIndex === sectionsOrder.length - 1) {
        nextBtn.style.display = "none";
    } else {
        nextBtn.style.display = "inline-block";
    }
}