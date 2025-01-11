document.addEventListener('DOMContentLoaded', () => {
    const currentPage = window.location.pathname.split('/').pop();

    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const sideNav = document.querySelector('.side-nav');
    const header = document.querySelector('.header');

    // Ensure the navbar is visible on non-index pages
    if (currentPage !== 'index.html') {
        header.classList.add('visible');
    }

    // Scroll Event: Show/Hide Navbar
    let lastScrollTop = 0;

    window.addEventListener('scroll', () => {
        const scrollPosition = window.scrollY;
        const introHeight = document.getElementById('intro') ? document.getElementById('intro').clientHeight : 0;

        if (scrollPosition > introHeight || currentPage !== 'index.html') {
            header.classList.add('visible');
        } else {
            header.classList.remove('visible');
        }

        if (scrollPosition > lastScrollTop && scrollPosition > introHeight) {
            header.style.top = '-100px'; // Hide on scroll down
        } else {
            header.style.top = '0'; // Show on scroll up
        }

        lastScrollTop = scrollPosition <= 0 ? 0 : scrollPosition;
    });

    // Menu Toggle Click Event
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        menuToggle.classList.toggle('open');
    });

    // Close Menu on Outside Click
    document.addEventListener('click', (event) => {
        if (
            !menuToggle.contains(event.target) && // Click is not on the toggle button
            !navLinks.contains(event.target) // Click is not inside the navigation links
        ) {
            navLinks.classList.remove('active');
            menuToggle.classList.remove('open');
        }
    });

    // Close Menu on Navigation Link Click
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            menuToggle.classList.remove('open');
        });
    });

    // Ensure dropdown menu works on smaller screens
    const dropdowns = document.querySelectorAll('.dropdown > .nav-link');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent default link behavior
            const dropdownMenu = dropdown.nextElementSibling;
            if (dropdownMenu) {
                dropdownMenu.classList.toggle('active');
            }
        });
    });
});
