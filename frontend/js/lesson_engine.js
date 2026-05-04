let currentLesson = 1;
let currentSectionIndex = 0;

const sectionsOrder = [
    "intro",
    "outcomes",
    "demo",
    "practice",
    "review"
];


// -------------------------
// RESUME SESSION (optional use)
// -------------------------
async function resumeSession() {

    const res = await fetch("http://127.0.0.1:5000/api/user/progress", {
        credentials: "include"
    });

    const data = await res.json();

    if (!data.success) return;

    currentLesson = data.progress.last_lesson || 1;

    const idx = sectionsOrder.indexOf(data.progress.last_section);
    currentSectionIndex = idx === -1 ? 0 : idx;

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

    title.innerText = `${data.lesson_title} - ${section.toUpperCase()}`;

    const content = data.data;

    // always reset UI state
    document.querySelector(".row").style.display = "flex";

    if (section === "intro") {
        box.innerHTML = `<p>${content.content}</p>`;
    }

    if (section === "outcomes") {
        box.innerHTML = `
            <ul>
                ${content.content.map(o => `<li>${o}</li>`).join("")}
            </ul>
        `;
    }

    if (section === "demo") {
        box.innerHTML = `
            <pre>${content.code}</pre>
            <p>${content.explanation}</p>
        `;
    }

    if (section === "practice") {
        tutor.classList.remove("hidden");
        box.innerHTML = `<p>${content.task}</p>`;
    }

    if (section === "review") {
        tutor.classList.add("hidden");

        box.innerHTML = `
            <p>${content.summary}</p>
            <h3>Lesson Complete ✓</h3>
            <button onclick="finishLesson()">Finish Lesson</button>
        `;
    }
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
            section: section
        })
    });
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
// INIT FROM URL
// -------------------------
async function initLessonFromURL() {

    await checkLogin();

    const params = new URLSearchParams(window.location.search);
    const id = parseInt(params.get("id"));

    if (!id) {
        window.location.href = "/index.html";
        return;
    }

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

    await loadSection();
}