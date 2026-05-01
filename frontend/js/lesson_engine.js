let currentLesson = 1;
let currentSectionIndex = 0;

let completedLessons = [];

const sectionsOrder = [
    "intro",
    "outcomes",
    "demo",
    "practice",
    "review"
];


// -------------------------
// RESUME SESSION
// -------------------------
async function resumeSession() {

    const res = await fetch("http://127.0.0.1:5000/api/user/resume", {
        credentials: "include"
    });

    const data = await res.json();

    if (!data.success) return;

    currentLesson = parseInt(data.last_lesson);

    let idx = sectionsOrder.indexOf(data.last_section);
    currentSectionIndex = idx === -1 ? 0 : idx;

    document.getElementById("lessonSelect").value = currentLesson;

    await loadCompletedLessons();
    await loadSection();
}


// -------------------------
// LOAD COMPLETED LESSONS
// -------------------------
async function loadCompletedLessons() {

    const res = await fetch("http://127.0.0.1:5000/api/user/completed", {
        credentials: "include"
    });

    const data = await res.json();

    if (data.success) {
        completedLessons = data.completed.map(Number);
    }

    lockLessons();
}


// -------------------------
// LOCK LESSONS
// -------------------------
function lockLessons() {

    const select = document.getElementById("lessonSelect");

    select.querySelectorAll("option").forEach(option => {

        const id = parseInt(option.value);

        if (id === 1) return;

        if (!completedLessons.includes(id - 1)) {
            option.disabled = true;
            option.style.opacity = "0.4";
        } else {
            option.disabled = false;
            option.style.opacity = "1";
        }
    });
}


// -------------------------
// START LESSON
// -------------------------
async function startLesson() {
    await loadLessons();
    currentLesson = parseInt(document.getElementById("lessonSelect").value);
    currentSectionIndex = 0;
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

    title.innerText = `${data.lesson_title} - ${section.toUpperCase()}`;

    const content = data.data;

    if (section === "intro") box.innerHTML = `<p>${content.content}</p>`;

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
        document.getElementById("tutorCard").classList.remove("hidden");
        box.innerHTML = `<p>${content.task}</p>`;
    }

    if (section === "review") {
        document.getElementById("tutorCard").classList.add("hidden");

        box.innerHTML = `
            <p>${content.summary}</p>
            <h3>Lesson Complete ✓</h3>
            <button onclick="markProgress()">Finish Lesson</button>
        `;
    }}


// -------------------------
// NEXT SECTION
// -------------------------
async function nextSection() {

    // SAVE PROGRESS ON EVERY STEP
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

    await fetch("http://127.0.0.1:5000/api/lesson/progress", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        credentials: "include",
        body: JSON.stringify({
            lesson_id: currentLesson,
            section: sectionsOrder[currentSectionIndex]
        })
    });
}

// -------------------------
// LOAD LESSONS
// -------------------------
async function loadLessons() {
    const res = await fetch("http://127.0.0.1:5000/api/user/progress", {
        credentials: "include"
    });

    const data = await res.json();

    const select = document.getElementById("lessonSelect");

    const completed = data.progress?.completed_lessons || [];

    for (let i = 0; i < select.options.length; i++) {
        const lessonId = parseInt(select.options[i].value);

        if (lessonId > 1 && !completed.includes(lessonId - 1)) {
            select.options[i].disabled = true;
        } else {
            select.options[i].disabled = false;
        }
    }
}