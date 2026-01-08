(function() {
    "use strict";

    /**
     * Initialize TomSelect for exercise selects inside session forms.
     * Skips elements that already have TomSelect initialized.
     */
    function initExerciseSelects() {
        document.querySelectorAll("select.js-exercise-select").forEach((el) => {
            if (el.tomselect) return;

            new TomSelect(el, {
                placeholder: "Select exercise...",
                closeAfterSelect: true,
                maxItems: 1,
                highlight: true,
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

    // Handle add/remove exercise clicks - wait for HTMX to complete then init
    document.body.addEventListener("click", (event) => {
        if (event.target.closest(".js-add-exercise") || event.target.closest(".js-remove-exercise")) {
            // Wait for HTMX to complete the swap (500ms should be enough)
            setTimeout(() => {
                initExerciseSelects();
            }, 500);
        }
    });
})();
