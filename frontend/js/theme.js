// -------------------------
// LOAD THEME
// -------------------------
async function loadTheme() {

    try {

        const res = await fetch(
            "http://127.0.0.1:5000/api/user/theme",
            {
                credentials: "include"
            }
        );

        const data = await res.json();

        const theme = data.theme || "light";

        document.body.setAttribute(
            "data-theme",
            theme
        );

        updateThemeButton(theme);

    } catch {

        document.body.setAttribute(
            "data-theme",
            "light"
        );
    }
}


// -------------------------
// TOGGLE THEME
// -------------------------
async function toggleTheme() {

    const current =
        document.body.getAttribute("data-theme");

    const next =
        current === "dark"
            ? "light"
            : "dark";

    document.body.setAttribute(
        "data-theme",
        next
    );

    updateThemeButton(next);

    try {

        await fetch(
            "http://127.0.0.1:5000/api/user/theme",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify({
                    theme: next
                })
            }
        );

    } catch (err) {
        // fallback to default theme if saving fails
        document.body.setAttribute(
            "data-theme",
            "light"
        );
    }
}


// -------------------------
// BUTTON TEXT
// -------------------------
function updateThemeButton(theme) {

    const btn =
        document.getElementById("themeToggle");

    if (!btn) return;

    btn.innerText =
        theme === "dark"
            ? "☀️ Light Mode"
            : "🌙 Dark Mode";
}


// -------------------------
// INIT
// -------------------------
document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadTheme();

        const btn =
            document.getElementById("themeToggle");

        if (btn) {

            btn.addEventListener(
                "click",
                toggleTheme
            );
        }
    }
);