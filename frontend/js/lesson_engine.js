// -------------------------
// LESSON ENGINE
// -------------------------
let currentLesson = null;
window.currentLessonId = null;
let currentSectionIndex = 0;

// This variable tracks whether the user has completed the coding task in the practice section. It is used to prevent users from navigating to the next section without completing the required task, ensuring that they engage with the material as intended.
let lessonProgress = {}; // per-lesson progress map

// This variable tracks whether the user has completed the coding task in the practice section. It is used to prevent users from navigating to the next section without completing the required task, ensuring that they engage with the material as intended.
const sectionsOrder = [
    "intro",
    "outcomes",
    "demo",
    "practice",
    "review"
];


// -------------------------
// INIT LESSON
// This function initializes the lesson by checking the user's login status, retrieving the lesson ID from the URL, verifying access to the lesson, loading the user's progress, and then loading the first section of the lesson. It ensures that only authorized users can access the lesson content and that their progress is properly tracked and displayed.
// -------------------------
async function initLessonFromURL() {

    // Check if the user is logged in and redirect to login page if not
    await checkLogin();

    // Initialize lesson progress tracking variables
    lessonCompleted = false;

    // Retrieve the lesson ID from the URL query parameters
    const params = new URLSearchParams(window.location.search);
    const id = Number(params.get("id"));

    // If no valid lesson ID is found in the URL, redirect the user to the index page
    if (!id) {
        window.location.href = "/index.html";
        return;
    }

    // -------------------------
    // GET LESSON ACCESS
    // This block checks if the user has access to the requested lesson by fetching the user's lesson status from the backend API. If the lesson is locked, it alerts the user and redirects them to the index page. This ensures that users can only access lessons they have unlocked, maintaining the integrity of the learning path.
    // -------------------------
    currentLesson = id;
    window.currentLessonId = currentLesson;
    currentSectionIndex = 0;

    // Fetch the user's lesson status from the backend API to check if the requested lesson is unlocked
    const res = await fetch("http://127.0.0.1:5000/api/user/lesson-status", {
        credentials: "include"
    });

    // Parse the JSON response from the server to get the list of lessons and their access status
    const data = await res.json();

    // Find the requested lesson in the list of lessons returned by the server
    const lesson = data.lessons.find(l => l.id === id);

    // If the lesson is not found or is locked, alert the user and redirect them to the index page
    if (!lesson || !lesson.unlocked) {
        alert("🔒 Lesson locked");
        window.location.href = "/index.html";
        return;
    }


    // -------------------------
    // LOAD PROGRESS (SAFE)
    // This block loads the user's progress for the current lesson by fetching it from the backend API. It ensures that the progress data is properly formatted and stored in a way that allows for easy access and updating as the user navigates through the lesson sections. This allows users to resume their progress if they leave and return to the lesson later.
    // -------------------------
    const progressRes = await fetch("http://127.0.0.1:5000/api/user/progress", {
        credentials: "include"
    });

    // Parse the JSON response from the server to get the user's progress data for lessons
    const progressData = await progressRes.json();

    // Convert the progress data into a format that allows for easy access and updating, ensuring that lesson IDs are treated as strings to avoid issues with JavaScript object keys
    lessonProgress = Object.fromEntries(
        Object.entries(progressData.progress?.lessons || {})
            .map(([k, v]) => [String(k), v])
    );

    // Load the first section of the lesson after successfully retrieving the user's progress
    await loadSection();
}

// -------------------------
// LOAD SECTION
// This function loads the content of the current section of the lesson by fetching it from the backend API. It updates the UI to display the section content, handles navigation visibility based on the current section, and ensures that the user can only access sections in the correct order. It also manages the display of the tutor card and navigation buttons based on the section being viewed.
// -------------------------
async function loadSection() {

    // Get the current section name based on the current section index and the predefined order of sections
    const section =
        sectionsOrder[currentSectionIndex];

        // Fetch the content for the current section of the lesson from the backend API, ensuring that the request includes credentials for authentication
    const res = await fetch(
        `http://127.0.0.1:5000/api/lesson/${currentLesson}/section/${section}`,
        {
            credentials: "include"
        }
    );

    // Parse the JSON response from the server to get the content for the current section of the lesson
    const data = await res.json();

    // Get references to various UI elements that will be updated with the section content and navigation controls
    const box =
        document.getElementById("lessonContent");

        // Update the lesson title in the UI to reflect the current lesson and section being viewed, providing context to the user about where they are in the lesson
    const title =
        document.getElementById("lessonTitle");

        // Get references to the tutor card, navigation row, and navigation buttons to manage their visibility and content based on the current section of the lesson
    const tutor =
        document.getElementById("tutorCard");

        // Get references to the navigation row and buttons to manage their visibility based on the current section of the lesson, ensuring that users can only navigate to appropriate sections and that the UI reflects their current position in the lesson
    const nav =
        document.querySelector(".row");

        // Get references to the back and next buttons to manage their visibility and functionality based on the current section of the lesson, allowing users to navigate through the lesson in a structured way while preventing access to sections they have not yet reached
    const backBtn =
        document.getElementById("backBtn");

        // Get a reference to the next button to manage its visibility based on the current section of the lesson, ensuring that users can only proceed to the next section after completing the current one and that the UI provides clear navigation cues
    const nextBtn =
        document.getElementById("nextBtn");

        // Update the lesson title in the UI to reflect the current lesson and section being viewed, providing context to the user about where they are in the lesson
    title.innerText =
        `${data.lesson_title} - ${section.toUpperCase()}`;

        // Get the content for the current section of the lesson from the parsed JSON response, which will be used to update the UI with the appropriate information and tasks for the user to engage with based on the section they are currently viewing
    const content = data.data;

    // Hide the tutor card by default, and only show it for the practice section where it is needed to provide guidance and support to the user as they work through the coding task. This helps to keep the UI clean and focused on the content for other sections while providing necessary assistance during practice.
    tutor.classList.add("hidden");

    // Show the navigation row by default, and manage its visibility based on the current section of the lesson to ensure that users have access to navigation controls when appropriate, while hiding them during sections like the review where they are not needed. This helps to guide users through the lesson in a structured way while keeping the UI clean and focused on the content.
    nav.style.display = "flex";

    // -------------------------
    // INTRO
    // This block handles the content and UI updates for the "intro" section of the lesson. It checks if there is saved progress for the current lesson and displays a resume option if the user has previously reached a different section. It then updates the lesson content in the UI with the introduction text, providing users with an overview of what they will learn in the lesson and allowing them to easily resume where they left off if they have previously accessed the lesson.
    // -------------------------
    if (section === "intro") {

        // Check if there is saved progress for the current lesson and display a resume option if the user has previously reached a different section
        const savedSection =
            lessonProgress[String(currentLesson)];

            // Initialize a variable to hold the HTML for the resume option, which will be displayed if the user has saved progress for the current lesson and has previously reached a different section than the intro
        let resumeUI = "";

        // If there is saved progress for the current lesson and it is not the intro section, create a resume option that allows the user to jump to where they left off in the lesson, providing a convenient way for users to continue their learning without having to manually navigate through the sections they have already completed
        if (
            savedSection &&
            savedSection !== "intro"
        ) {

            // Create the HTML for the resume option, which includes a message indicating where the user previously reached in the lesson and a button that allows them to jump to that section directly, enhancing the user experience by providing a clear and easy way to resume their progress
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

        // Update the lesson content in the UI with the introduction text, providing users with an overview of what they will learn in the lesson and allowing them to easily resume where they left off if they have previously accessed the lesson
        box.innerHTML = `
            ${resumeUI}
            <p>${content.content}</p>
        `;
    }

    // -------------------------
    // OUTCOMES
    // This block handles the content and UI updates for the "outcomes" section of the lesson. It updates the lesson content in the UI to display a list of learning outcomes for the lesson, providing users with a clear understanding of what they will achieve by completing the lesson and helping to set expectations for their learning journey.
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
    // This block handles the content and UI updates for the "demo" section of the lesson. It updates the lesson content in the UI to display a code demonstration along with an explanation, providing users with a practical example of the concepts being taught in the lesson and helping to reinforce their understanding through visual and contextual learning.
    // -------------------------
    if (section === "demo") {

        box.innerHTML = `
            <pre>${content.code}</pre>
            <p>${content.explanation}</p>
        `;
    }

    // -------------------------
    // PRACTICE
    // This block handles the content and UI updates for the "practice" section of the lesson. It shows the tutor card to provide guidance and support to the user as they work through the coding task, and updates the lesson content in the UI with the task description, allowing users to engage with a practical coding exercise that reinforces the concepts taught in the lesson and provides an opportunity for hands-on learning.
    // -------------------------
    if (section === "practice") {

        tutor.classList.remove("hidden");

        box.innerHTML = `
            <p>${content.task}</p>
        `;
    }

    // -------------------------
    // REVIEW
    // This block handles the content and UI updates for the "review" section of the lesson. It hides the navigation controls to focus the user's attention on the review content, and updates the lesson content in the UI with a summary of what was covered in the lesson, providing users with a recap of the key concepts and takeaways from the lesson to reinforce their learning and help solidify their understanding of the material.
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
    // This block manages the visibility of navigation controls based on the current section of the lesson. It hides the back button on the intro section to prevent users from navigating to a previous section that does not exist, and hides all navigation controls on the review section to focus the user's attention on the review content. For all other sections, it ensures that the navigation controls are visible, allowing users to navigate through the lesson in a structured way while providing clear cues about their current position in the lesson.
    // -------------------------

    // Hide Back on intro
    if (currentSectionIndex === 0) {

        // Hide the back button on the intro section to prevent users from navigating to a previous section that does not exist, ensuring that the navigation controls are contextually appropriate and that users have a clear understanding of their position in the lesson without confusion about available navigation options
        backBtn.style.display = "none";

    } else {

        // Show back button for all other sections except intro, allowing users to navigate back to previous sections as needed while ensuring that they cannot navigate to a non-existent section before the intro
        backBtn.style.display = "inline-block";
    }

    // Hide all nav on review
    if (section === "review") {

        // Hide the navigation controls on the review section to focus the user's attention on the review content, providing a clear and distraction-free environment for users to reflect on what they have learned in the lesson
        nav.style.display = "none";

    } else {

        // Show navigation controls for all sections except review, allowing users to navigate through the lesson in a structured way while ensuring that they have access to appropriate navigation options based on their current position in the lesson
        nav.style.display = "flex";

        // Show next button for all sections except review, allowing users to proceed to the next section after completing the current one while ensuring that they cannot navigate to a non-existent section after the review
        nextBtn.style.display =
            "inline-block";
    }
}
// -------------------------
// SAVE PROGRESS
// This function saves the user's progress for the current lesson by sending a POST request to the backend API with the current lesson ID and section. It updates the local progress tracking variable to reflect the user's current position in the lesson, ensuring that their progress is properly tracked and can be resumed if they leave and return to the lesson later.
// -------------------------
async function markProgress() {

    // Get the current section name based on the current section index and the predefined order of sections, which will be sent to the backend API to update the user's progress for the current lesson
    const section = sectionsOrder[currentSectionIndex];

    // Send a POST request to the backend API to save the user's progress for the current lesson, including the lesson ID and the current section, ensuring that the request includes credentials for authentication and that the progress data is properly formatted as JSON
    await fetch("http://127.0.0.1:5000/api/lesson/progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
            lesson_id: currentLesson,
            section
        })
    });

    // Update the local progress tracking variable to reflect the user's current position in the lesson, ensuring that the progress is properly tracked and can be resumed if they leave and return to the lesson later
    lessonProgress[String(currentLesson)] = section;
}


// -------------------------
// NEXT SECTION
// This function handles the navigation to the next section of the lesson. It checks if the user has completed the required task in the practice section before allowing them to proceed, ensuring that users engage with the material as intended. If the user is allowed to proceed, it saves their progress and loads the next section of the lesson, providing a structured learning experience while maintaining the integrity of the lesson flow.
// -------------------------
async function nextSection() {

    // Get the current section name based on the current section index and the predefined order of sections, which will be used to determine if the user has completed the required task in the practice section before allowing them to proceed to the next section
    const currentSection =
        sectionsOrder[currentSectionIndex];

    // -------------------------
    // LOCK PRACTICE SECTION
    // This block checks if the user is currently in the practice section and has not completed the required coding task. If the user has not completed the task, it alerts them and prevents them from proceeding to the next section, ensuring that users engage with the material as intended and do not skip important learning activities that are crucial for their understanding of the concepts being taught in the lesson.
    // -------------------------
    if (
        currentSection === "practice" &&
        !lessonCompleted
    ) {

        // Alert the user that they need to complete the coding task before they can proceed to the next section, providing a clear message about the requirement and encouraging them to engage with the practice material to reinforce their learning
        alert("⚠️ Complete the coding task before continuing.");
        return;
    }

    // -------------------------
    // MOVE TO NEXT SECTION
    // If the user is allowed to proceed to the next section, save their progress and load the next section of the lesson, providing a structured learning experience while maintaining the integrity of the lesson flow and ensuring that users can easily track their progress through the lesson.
    // -------------------------
    if (currentSectionIndex < sectionsOrder.length - 1) {

        // save progress FIRST
        await markProgress();

        // Move to the next section by incrementing the current section index and loading the next section of the lesson, allowing users to continue their learning journey in a structured way while ensuring that their progress is properly tracked and saved before they proceed
        currentSectionIndex++;

        // Load the next section of the lesson after successfully saving the user's progress, providing a seamless transition to the next part of the lesson while ensuring that their progress is not lost
        await loadSection();
    }
}

// -------------------------
// FINISH LESSON
// This function handles the completion of the lesson by sending a POST request to the backend API to update the user's progress to indicate that they have completed the lesson. After successfully updating the progress, it redirects the user to the index page, providing a clear endpoint for the lesson and allowing users to easily return to the main page after finishing their learning experience.
// -------------------------
async function finishLesson() {

    // Send a POST request to the backend API to update the user's progress to indicate that they have completed the lesson, ensuring that the request includes credentials for authentication and that the progress data is properly formatted as JSON
    await fetch("http://127.0.0.1:5000/api/lesson/progress", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
            lesson_id: currentLesson,
            section: "review"
        })
    });

    // Redirect the user to the index page after successfully updating their progress, providing a clear endpoint for the lesson and allowing users to easily return to the main page after finishing their learning experience
    window.location.href = "/index.html";
}


// -------------------------
// EXIT LESSON
// This function allows the user to exit the lesson and return to the index page. It first saves the user's progress to ensure that their current position in the lesson is not lost, and then redirects them to the index page, providing a convenient way for users to leave the lesson while ensuring that their progress is properly tracked and can be resumed later if they choose to return to the lesson.
// -------------------------
async function exitLesson() {

    // Save the user's progress before exiting the lesson to ensure that their current position in the lesson is not lost, allowing them to easily resume where they left off if they choose to return to the lesson later
    await markProgress(); // ensures backend is updated first
    window.location.href = "/index.html";
}


// -------------------------
// JUMP TO SECTION
// This function allows the user to jump directly to a specific section of the lesson by providing the section name. It checks if the provided section name is valid and, if so, updates the current section index and loads the specified section of the lesson. This provides users with a convenient way to navigate to specific sections of the lesson without having to go through each section sequentially, while still ensuring that they can only jump to valid sections within the lesson.
// -------------------------
function jumpToSection(sectionName) {

    // Get the index of the specified section name from the predefined order of sections, which will be used to update the current section index and load the specified section of the lesson if it is valid
    const idx = sectionsOrder.indexOf(sectionName);

    // If the specified section name is valid (i.e., it exists in the predefined order of sections), update the current section index and load the specified section of the lesson, allowing users to jump directly to specific sections of the lesson while ensuring that they can only jump to valid sections within the lesson
    if (idx !== -1) {
        currentSectionIndex = idx;
        loadSection();
    }
}

// -------------------------
// PREVIOUS SECTION
// This function allows the user to navigate to the previous section of the lesson. It checks if the current section index is greater than 0 to ensure that there is a previous section to navigate to, and if so, it decrements the current section index and loads the previous section of the lesson. This provides users with a convenient way to go back and review previous sections of the lesson as needed while ensuring that they cannot navigate to a non-existent section before the intro.
// -------------------------
async function prevSection() {

    // Check if the current section index is greater than 0 to ensure that there is a previous section to navigate to, preventing users from navigating to a non-existent section before the intro and ensuring that the navigation controls are contextually appropriate based on the user's current position in the lesson
    if (currentSectionIndex <= 0) return;

    // Move to the previous section by decrementing the current section index and loading the previous section of the lesson, allowing users to go back and review previous sections of the lesson as needed while ensuring that they cannot navigate to a non-existent section before the intro
    currentSectionIndex--;
    await loadSection();
}
