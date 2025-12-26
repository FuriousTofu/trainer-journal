// ----- Button with .js-go behaves like a link. Works for one button on the page -----
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector(".js-go");
    if (!btn) return;

    btn.addEventListener("click", () => {
        const url = btn.dataset.url;
        if (url) window.location.assign(url);
    });
});