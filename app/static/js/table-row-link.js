// ----- Make table rows clickable -----
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.table-row-link').forEach((row) => {
        row.addEventListener('click', () => {
            const url = row.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
});