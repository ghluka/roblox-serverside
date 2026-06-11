(function () {
    const storageKey = "nettss_theme";
    const fallbackTheme = "violet";
    const validThemes = new Set(["violet", "cyber", "ember", "ocean", "mono"]);
    const buttons = Array.from(document.querySelectorAll("[data-theme-option]"));

    function normalizeTheme(theme) {
        return validThemes.has(theme) ? theme : fallbackTheme;
    }

    function applyTheme(theme) {
        const selectedTheme = normalizeTheme(theme);
        document.documentElement.dataset.theme = selectedTheme;
        localStorage.setItem(storageKey, selectedTheme);

        buttons.forEach(button => {
            const selected = button.dataset.themeOption === selectedTheme;
            button.classList.toggle("active", selected);
            button.setAttribute("aria-pressed", selected ? "true" : "false");
        });

        return selectedTheme;
    }

    function saveTheme(theme) {
        fetch("/api/theme", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ theme })
        }).catch(error => console.error("Failed to save theme:", error));
    }

    function setTheme(theme) {
        const selectedTheme = applyTheme(theme);
        saveTheme(selectedTheme);
    }

    buttons.forEach(button => {
        button.addEventListener("click", () => setTheme(button.dataset.themeOption));
    });

    applyTheme(window.NettSSTheme || localStorage.getItem(storageKey) || fallbackTheme);
}());
