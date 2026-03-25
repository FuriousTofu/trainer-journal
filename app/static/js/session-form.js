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

    function initTagSelect() {
        var el = document.getElementById("input-tags");
        if (!el || el.tomselect) return;

        new TomSelect(el, {
            plugins: ["remove_button"],
            maxItems: 4,
            placeholder: "Select tags...",
            render: {
                option: function(data, escape) {
                    return '<div><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:'
                        + escape(data.color) + ';margin-right:6px;vertical-align:middle;"></span>'
                        + escape(data.text) + '</div>';
                },
                item: function(data, escape) {
                    return '<div style="background:' + escape(data.color)
                        + ';color:#fff;border-radius:4px;padding:2px 6px;margin:2px;">'
                        + escape(data.text) + '</div>';
                }
            },
            onInitialize: function() {
                // Populate color data from data attributes
                var self = this;
                Object.keys(self.options).forEach(function(key) {
                    var optEl = el.querySelector('option[value="' + key + '"]');
                    if (optEl) {
                        self.options[key].color = optEl.dataset.color || "#6B7280";
                    }
                });
            }
        });
    }

    // Initial page load
    document.addEventListener("DOMContentLoaded", () => {
        initExerciseSelects();
        initTagSelect();
        // Delay to ensure TomSelect has synced values to the underlying selects
        setTimeout(triggerExerciseHistoryRefresh, 100);
    });

    function triggerExerciseHistoryRefresh() {
        document
            .querySelectorAll('select[name^="exercises-"][name$="-exercise"]')
            .forEach(function (sel) {
                var value = sel.tomselect ? sel.tomselect.getValue() : sel.value;
                if (value && value !== "0" && value !== "") {
                    htmx.trigger(sel, "change");
                }
            });
    }

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
                    triggerExerciseHistoryRefresh();
                    document.body.removeEventListener("htmx:afterSettle", handleRemove);
                }
            });
        }
    });
})();
