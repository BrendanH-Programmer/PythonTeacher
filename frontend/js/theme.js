// -------------------------
// LOAD THEME
// This function is responsible for loading the user's preferred theme (light or dark) when the page is loaded. It makes an API call to retrieve the user's theme preference from the backend and applies it to the document body. If the API call fails for any reason, it defaults to the light theme. This ensures that users have a consistent visual experience based on their preferences while also providing a fallback option in case of any issues with retrieving the theme preference.
// -------------------------
async function loadTheme() {

    // Attempt to fetch the user's theme preference from the backend API and apply it to the document body, providing a personalized visual experience based on the user's settings. If the API call fails for any reason (e.g., network issues, server errors), the function will catch the error and default to applying the light theme, ensuring that the user still has a functional and visually consistent experience even if their specific theme preference cannot be retrieved.
    try {

        // Make a GET request to the backend API to retrieve the user's theme preference, including credentials to ensure that the request is authenticated and can access the user's settings. The response is expected to be in JSON format, containing a "theme" property that indicates the user's preferred theme (e.g., "light" or "dark").
        const res = await fetch(
            "http://127.0.0.1:5000/api/user/theme",
            {
                // Include credentials in the request to ensure that it is authenticated and can access the user's settings, allowing the backend to identify the user and return their specific theme preference. This is important for providing a personalized experience based on the user's preferences while also ensuring that the request is secure and properly authenticated.
                credentials: "include"
            }
        );

        // Parse the JSON response from the server to extract the user's theme preference, which will be used to apply the appropriate theme to the document body. The response is expected to contain a "theme" property that indicates the user's preferred theme (e.g., "light" or "dark"), and if this property is not present, it defaults to "light" to ensure that there is always a valid theme applied.
        const data = await res.json();

        // Extract the user's theme preference from the response data, defaulting to "light" if the "theme" property is not present. This ensures that there is always a valid theme applied to the document body, providing a consistent visual experience for the user even if their specific theme preference cannot be retrieved from the backend.
        const theme = data.theme || "light";

        // Apply the user's theme preference to the document body by setting the "data-theme" attribute, which can be used in CSS to apply the appropriate styles based on the theme. This allows for a personalized visual experience based on the user's settings while also providing a consistent and visually appealing interface.
        document.body.setAttribute(
            "data-theme",
            theme
        );

        // Update the theme toggle button text to reflect the current theme, providing a clear indication to the user of their current theme and allowing them to easily switch between themes as needed. This enhances the user experience by making it easy for users to understand their current theme and providing a convenient way to toggle between themes based on their preferences.
        updateThemeButton(theme);

        // If the API call to retrieve the user's theme preference fails for any reason (e.g., network issues, server errors), the function will catch the error and default to applying the light theme, ensuring that the user still has a functional and visually consistent experience even if their specific theme preference cannot be retrieved. This provides a fallback option that maintains a good user experience while also allowing for personalization when possible.
    } catch {

        // Fallback to light theme if there is an error fetching the user's theme preference, ensuring that the user still has a functional and visually consistent experience even if their specific theme preference cannot be retrieved from the backend. This provides a default visual style that is widely accepted and ensures that the interface remains usable and visually appealing in the absence of specific user preferences.
        document.body.setAttribute(
            "data-theme",
            "light"
        );
    }
}


// -------------------------
// TOGGLE THEME
// This function allows the user to toggle between light and dark themes by updating the "data-theme" attribute on the document body and sending the updated theme preference to the backend API. It also updates the theme toggle button text to reflect the current theme, providing a clear indication to the user of their current theme and allowing them to easily switch between themes as needed. If there is an error while saving the user's theme preference to the backend, it falls back to applying the light theme to ensure that the user still has a functional and visually consistent experience.
// -------------------------
async function toggleTheme() {

    // Get the current theme from the "data-theme" attribute on the document body, which indicates whether the current theme is "light" or "dark". This value will be used to determine the next theme to apply when the user toggles the theme, allowing for a seamless transition between themes based on the user's interaction.
    const current =
        document.body.getAttribute("data-theme");

        // Determine the next theme to apply based on the current theme, toggling between "light" and "dark". If the current theme is "dark", the next theme will be "light"; if the current theme is "light", the next theme will be "dark". This logic allows for a simple and intuitive way for users to switch between themes based on their preferences, providing a personalized visual experience.
    const next =
        current === "dark"
            ? "light"
            : "dark";

            // Update the "data-theme" attribute on the document body to apply the next theme, allowing for a seamless transition between themes based on the user's interaction. This will trigger any CSS styles that are defined based on the "data-theme" attribute, providing a visually appealing and personalized experience for the user.
    document.body.setAttribute(
        "data-theme",
        next
    );

    // Update the theme toggle button text to reflect the new theme, providing a clear indication to the user of their current theme and allowing them to easily switch between themes as needed. This enhances the user experience by making it easy for users to understand their current theme and providing a convenient way to toggle between themes based on their preferences.
    updateThemeButton(next);

    // Attempt to save the user's theme preference to the backend API, allowing for a personalized experience based on the user's settings. If there is an error while saving the user's theme preference (e.g., network issues, server errors), the function will catch the error and fall back to applying the light theme, ensuring that the user still has a functional and visually consistent experience even if their specific theme preference cannot be saved to the backend.
    try {

        // Make a POST request to the backend API to save the user's theme preference, including credentials to ensure that the request is authenticated and can access the user's settings. The request body contains the new theme preference in JSON format, allowing the backend to update the user's settings accordingly. This ensures that the user's theme preference is persisted across sessions and provides a personalized experience based on their settings.
        await fetch(
            "http://127.0.0.1:5000/api/user/theme",
            {
                // Include credentials in the request to ensure that it is authenticated and can access the user's settings, allowing the backend to identify the user and update their specific theme preference. This is important for providing a personalized experience based on the user's preferences while also ensuring that the request is secure and properly authenticated.
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                // Include credentials in the request to ensure that it is authenticated and can access the user's settings, allowing the backend to identify the user and update their specific theme preference. This is important for providing a personalized experience based on the user's preferences while also ensuring that the request is secure and properly authenticated.
                credentials: "include",
                body: JSON.stringify({
                    theme: next
                })
            }
        );

        // If there is an error while saving the user's theme preference to the backend, the function will catch the error and fall back to applying the light theme, ensuring that the user still has a functional and visually consistent experience even if their specific theme preference cannot be saved to the backend. This provides a fallback option that maintains a good user experience while also allowing for personalization when possible.
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
// This function updates the text of the theme toggle button based on the current theme, providing a clear indication to the user of their current theme and allowing them to easily switch between themes as needed. If the current theme is "dark", the button text will indicate that clicking it will switch to "Light Mode"; if the current theme is "light", the button text will indicate that clicking it will switch to "Dark Mode". This enhances the user experience by making it easy for users to understand their current theme and providing a convenient way to toggle between themes based on their preferences.
// -------------------------
function updateThemeButton(theme) {

    // Get the theme toggle button element from the DOM, which will be used to update its text based on the current theme. If the button element is not found (e.g., it does not exist in the DOM), the function will return early to avoid any errors when trying to update the button text.
    const btn =
        document.getElementById("themeToggle");

        // If the theme toggle button element is not found in the DOM, return early to avoid any errors when trying to update the button text. This ensures that the function can safely handle cases where the button may not be present on the page without causing any issues or errors in the execution of the script.
    if (!btn) return;

    // Update the theme toggle button text based on the current theme, providing a clear indication to the user of their current theme and allowing them to easily switch between themes as needed. If the current theme is "dark", the button text will indicate that clicking it will switch to "Light Mode"; if the current theme is "light", the button text will indicate that clicking it will switch to "Dark Mode". This enhances the user experience by making it easy for users to understand their current theme and providing a convenient way to toggle between themes based on their preferences.
    btn.innerText =
        theme === "dark"
            ? "☀️ Light Mode"
            : "🌙 Dark Mode";
}


// -------------------------
// INIT
// This code initializes the theme functionality by adding an event listener for the "DOMContentLoaded" event, which ensures that the theme is loaded and the toggle button is set up once the DOM is fully loaded. It calls the loadTheme function to apply the user's preferred theme and sets up a click event listener on the theme toggle button to allow users to switch between themes as needed. This ensures that the theme functionality is properly initialized and ready for user interaction as soon as the page is loaded.
// -------------------------
document.addEventListener(

    // Listen for the "DOMContentLoaded" event to ensure that the theme is loaded and the toggle button is set up once the DOM is fully loaded, allowing for a seamless user experience where the user's preferred theme is applied and the toggle button is functional as soon as the page is ready.
    "DOMContentLoaded",
    () => {

        // Load the user's preferred theme when the page is loaded, applying it to the document body to provide a personalized visual experience based on the user's settings. If there is an error while loading the theme preference (e.g., network issues, server errors), it will fall back to applying the light theme to ensure that the user still has a functional and visually consistent experience.
        loadTheme();

        // Set up a click event listener on the theme toggle button to allow users to switch between themes as needed, providing a convenient way for users to customize their visual experience based on their preferences. If the theme toggle button is not found in the DOM, it will simply not set up the event listener, allowing the rest of the functionality to work without any issues.
        const btn =
        // Get the theme toggle button element from the DOM, which will be used to set up a click event listener that allows users to switch between themes as needed. If the button element is not found (e.g., it does not exist in the DOM), the function will simply not set up the event listener, allowing the rest of the functionality to work without any issues.
            document.getElementById("themeToggle");

            // If the theme toggle button element is found in the DOM, set up a click event listener that calls the toggleTheme function when the button is clicked, allowing users to switch between themes as needed. This provides a convenient way for users to customize their visual experience based on their preferences while ensuring that the functionality is only set up if the button exists on the page.
        if (btn) {

            // Set up a click event listener on the theme toggle button to allow users to switch between themes as needed, providing a convenient way for users to customize their visual experience based on their preferences. If the theme toggle button is not found in the DOM, it will simply not set up the event listener, allowing the rest of the functionality to work without any issues.
            btn.addEventListener(
                "click",
                toggleTheme
            );
        }
    }
);