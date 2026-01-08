/**
 * Initialize TomSelect for exercise selects inside session forms.
 * Works for:
 * - Add Session (empty rows)
 * - Edit Session (pre-filled rows)
 * - HTMX dynamically added rows
 */
function initExerciseSelects(root = document) {
    root.querySelectorAll(".js-exercise-select").forEach((el) => {
        if (el.tomselect) return;

        new TomSelect(el, {
            placeholder: "Select exercise...",
            closeAfterSelect: true,
            maxItems: 1,
            highlight: true,

        // Re-trigger native change event for HTMX
            onChange: () => {
                htmx.trigger(el, "change");
            }
        });
    });
}

// Initial page load
document.addEventListener("DOMContentLoaded", () => {
    initExerciseSelects();
});

// HTMX: after new exercise row is added
document.body.addEventListener("htmx:afterSwap", (event) => {
    initExerciseSelects(event.target);
});
