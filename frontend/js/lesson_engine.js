let currentLesson = null;
window.currentLessonId = null;
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

    lessonCompleted = false;

    const params = new URLSearchParams(window.location.search);
    const id = Number(params.get("id"));

    if (!id) {
        window.location.href = "/index.html";
        return;
    }

    // -------------------------
    // GET LESSON ACCESS
    // -------------------------
    currentLesson = id;
    window.currentLessonId = currentLesson;
    currentSectionIndex = 0;

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

    const section =
        sectionsOrder[currentSectionIndex];

    const res = await fetch(
        `http://127.0.0.1:5000/api/lesson/${currentLesson}/section/${section}`,
        {
            credentials: "include"
        }
    );

    const data = await res.json();

    const box =
        document.getElementById("lessonContent");

    const title =
        document.getElementById("lessonTitle");

    const tutor =
        document.getElementById("tutorCard");

    const nav =
        document.querySelector(".row");

    const backBtn =
        document.getElementById("backBtn");

    const nextBtn =
        document.getElementById("nextBtn");

    title.innerText =
        `${data.lesson_title} - ${section.toUpperCase()}`;

    const content = data.data;

    tutor.classList.add("hidden");

    nav.style.display = "flex";

    // -------------------------
    // INTRO
    // -------------------------
    if (section === "intro") {

        const savedSection =
            lessonProgress[String(currentLesson)];

        let resumeUI = "";

        if (
            savedSection &&
            savedSection !== "intro"
        ) {

            resumeUI = `
                <div class="resume-box">

                    <p>
                        You previously reached:
                        <strong>
                            ${savedSection.toUpperCase()}
                        </strong>
                    </p>

                    <button
                        onclick="jumpToSection('${savedSection}')">

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
                ${content.content
                    .map(o => `<li>${o}</li>`)
                    .join("")}
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

        box.innerHTML = `
            <p>${content.task}</p>
        `;
    }

    // -------------------------
    // REVIEW
    // -------------------------
    if (section === "review") {

        nav.style.display = "none";

        box.innerHTML = `
            <div class="card">

                <h2>🎉 Lesson Complete</h2>

                <p>
                    ${content.summary}
                </p>

                <button onclick="finishLesson()">
                    Finish Lesson
                </button>

            </div>
        `;
    }

    // -------------------------
    // NAVIGATION VISIBILITY
    // -------------------------

    // Hide Back on intro
    if (currentSectionIndex === 0) {

        backBtn.style.display = "none";

    } else {

        backBtn.style.display = "inline-block";
    }

    // Hide all nav on review
    if (section === "review") {

        nav.style.display = "none";

    } else {

        nav.style.display = "flex";

        nextBtn.style.display =
            "inline-block";
    }
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

    const currentSection =
        sectionsOrder[currentSectionIndex];

    // -------------------------
    // LOCK PRACTICE SECTION
    // -------------------------
    if (
        currentSection === "practice" &&
        !lessonCompleted
    ) {

        alert("⚠️ Complete the coding task before continuing.");
        return;
    }

    // -------------------------
    // MOVE TO NEXT SECTION
    // -------------------------
    if (currentSectionIndex < sectionsOrder.length - 1) {

        // save progress FIRST
        await markProgress();

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
