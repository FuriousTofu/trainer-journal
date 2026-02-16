(function() {
    "use strict";

    function toggleExerciseFields(row, type) {
        var repsField = row.querySelector(".exercise-field-reps");
        var timeField = row.querySelector(".exercise-field-time");
        if (!repsField || !timeField) return;

        if (type === "time") {
            repsField.style.display = "none";
            timeField.style.display = "";
            // Clear hidden field to avoid sending both values
            var repsInput = repsField.querySelector("input");
            if (repsInput) repsInput.value = "";
        } else {
            repsField.style.display = "";
            timeField.style.display = "none";
            var timeInput = timeField.querySelector("input");
            if (timeInput) timeInput.value = "";
        }
    }

    function getExerciseType(value) {
        if (!value || !window.EXERCISE_TYPES) return "reps";
        return window.EXERCISE_TYPES[value] || "reps";
    }

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
                onChange: (value) => {
                    htmx.trigger(el, "change");
                    var row = el.closest(".exercise-row");
                    if (row) {
                        toggleExerciseFields(row, getExerciseType(value));
                    }
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
