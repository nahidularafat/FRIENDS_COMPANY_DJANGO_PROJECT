// This function runs when the entire HTML document has been loaded.
document.addEventListener('DOMContentLoaded', function() {

    // --- 1. Theme Toggle Functionality ---
    const themeToggleButton = document.getElementById('theme-toggle');
    
    if (themeToggleButton) {
        // This function sets the theme based on localStorage or OS preference
        const applyTheme = () => {
            if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.remove('dark');
            }
        };

        // Apply the theme on initial load
        applyTheme();

        // This event listener waits for a click on the theme toggle button.
        themeToggleButton.addEventListener('click', function() {
            // Toggle the 'dark' class on the root <html> element.
            document.documentElement.classList.toggle('dark');

            // Check the current theme and save it to localStorage for persistence.
            let theme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
            localStorage.setItem('color-theme', theme);
        });
    }


    // --- 2. Active Navigation Link Functionality ---
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;

    // Loop through all navigation links.
    navLinks.forEach(link => {
        // Check if the link's href is the same as the current path
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

});