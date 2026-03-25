// ----- Make table rows clickable -----
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.table-row-link').forEach((row) => {
        row.addEventListener('click', (e) => {
            if (e.target.closest('.toggle-paid') || e.target.closest('.toggle-status')) return;
            const url = row.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
});