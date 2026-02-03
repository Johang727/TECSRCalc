const prefers_dark = window.matchMedia("(prefers-color-scheme: dark)").matches;

function apply_dark(is_dark) {
    if (is_dark) {
        document.body.classList.add("dark-mode");
    } else {
        document.body.classList.remove("dark-mode");
    }
}

function init_theme() {
    const theme = localStorage.getItem("theme");

    switch (theme) {
        case "dark":
            apply_dark(true);
            break;
        case "light":
            apply_dark(false);
            break;
        default:
            apply_dark(prefers_dark);
            break;
    }
}

function toggle_theme() {
    const is_dark = document.body.classList.toggle("dark-mode");
    localStorage.setItem("theme", is_dark ? "dark" : "light");
}

init_theme();

document.addEventListener("DOMContentLoaded", function() {
    const toggle_button = document.getElementById("theme-toggle");

    toggle_button.addEventListener("click", toggle_theme);
});