// ----- Tooltip initialization -----
(() => {
    'use strict';
    const tooltipTriggerList = Array.from(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.forEach((tooltipTriggerEl) => {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
})();

// ----- Flash message auto-hide -----
document.addEventListener('DOMContentLoaded', () => {
    const flashContainer = document.getElementById('flash-container');
    if (flashContainer) {
        setTimeout(() => {
            flashContainer.style.transition = 'opacity 0.5s ease';
            flashContainer.style.opacity = '0';

            setTimeout(() => {
                flashContainer.remove();
            }, 500);

        }, 5000);
    }
});