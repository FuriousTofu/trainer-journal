(function() {
    "use strict";

    function initExerciseSelects(container = document) {
        container.querySelectorAll("select.js-exercise-select").forEach((el) => {
            if (el.tomselect) return;

            new TomSelect(el, {
                placeholder: "Select exercise...",
                closeAfterSelect: true,
                maxItems: 1,
                highlight: true,
                allowEmptyOption: false,
                create: true,
                onChange: () => {
                    htmx.trigger(el, "change");
                },
                createFilter: function(input) {
                    return input.length >= 3;
                },
            });
        });
    }

    // Initial page load
    document.addEventListener("DOMContentLoaded", () => {
        initExerciseSelects();
    });

    document.body.addEventListener("click", (event) => {
        const addBtn = event.target.closest(".js-add-exercise");
        const removeBtn = event.target.closest(".js-remove-exercise");

        if (addBtn) {
            document.body.addEventListener("htmx:afterSwap", function handleAdd(e) {
                if (e.detail.target.id === "exercise-wrapper") {
                    initExerciseSelects(e.detail.target);
                    document.body.removeEventListener("htmx:afterSwap", handleAdd);
                }
            });
        }
        // Used afterSettle because with afterSwap default select elements are not hidden properly yet
        if (removeBtn) {
            document.body.addEventListener("htmx:afterSettle", function handleRemove(e) {
                if (e.detail.target.id === "exercise-wrapper") {
                    initExerciseSelects(e.detail.target);
                    document.body.removeEventListener("htmx:afterSettle", handleRemove);
                }
            });
        }
    });
})();