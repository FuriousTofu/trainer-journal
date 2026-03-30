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

    // ── Drag-and-drop reordering ──────────────────────────────────────────

    function renumberRows() {
        var items = Array.from(
            document.querySelectorAll("#exercise-wrapper .exercise-item")
        );

        // Snapshot state before any mutation
        var plan = items.map(function(item, newIndex) {
            var row = item.querySelector(".exercise-row");
            var oldIndex = row.dataset.index;
            return {
                row: row,
                oldIndex: oldIndex,
                newIndex: String(newIndex),
                histDiv: item.querySelector("[id^='ex-history-']"),
            };
        });

        if (plan.every(function(p) { return p.oldIndex === p.newIndex; })) return;

        // Step 1: strip all history IDs to prevent conflicts during rename
        plan.forEach(function(p) {
            if (p.histDiv) p.histDiv.removeAttribute("id");
        });

        // Step 2: rename inputs/attrs and update HTMX bindings
        plan.forEach(function(p) {
            if (p.oldIndex === p.newIndex) return;

            p.row.querySelectorAll("[name^='exercises-']").forEach(function(el) {
                el.name = el.name.replace(
                    /^exercises-\d+-/,
                    "exercises-" + p.newIndex + "-"
                );
            });
            p.row.querySelectorAll("[id^='exercises-']").forEach(function(el) {
                el.id = el.id.replace(
                    /^exercises-\d+-/,
                    "exercises-" + p.newIndex + "-"
                );
            });
            p.row.querySelectorAll("[for^='exercises-']").forEach(function(el) {
                el.htmlFor = el.htmlFor.replace(
                    /^exercises-\d+-/,
                    "exercises-" + p.newIndex + "-"
                );
            });

            var sel = p.row.querySelector("[hx-target^='#ex-history-']");
            if (sel) {
                sel.setAttribute("hx-target", "#ex-history-" + p.newIndex);
                sel.setAttribute("hx-vals", '{"row_index": "' + p.newIndex + '"}');
            }

            var btn = p.row.querySelector(".js-remove-exercise");
            if (btn) {
                var v = JSON.parse(btn.getAttribute("hx-vals"));
                v.remove_index = p.newIndex;
                btn.setAttribute("hx-vals", JSON.stringify(v));
            }

            p.row.dataset.index = p.newIndex;
        });

        // Step 3: restore history IDs with correct new indices
        plan.forEach(function(p) {
            if (p.histDiv) p.histDiv.id = "ex-history-" + p.newIndex;
        });
    }

    function initSortable() {
        var wrapper = document.getElementById("exercise-wrapper");
        if (!wrapper) return;
        if (wrapper._sortable) {
            wrapper._sortable.destroy();
        }
        var isTouch = navigator.maxTouchPoints > 0;
        wrapper._sortable = new Sortable(wrapper, {
            handle: isTouch ? undefined : ".drag-handle",
            draggable: ".exercise-item",
            animation: 150,
            delay: isTouch ? 400 : 0,
            delayOnTouchOnly: true,
            forceFallback: isTouch,
            onEnd: renumberRows,
        });
        if (isTouch) {
            wrapper.addEventListener("contextmenu", function(e) { e.preventDefault(); });
        }
    }

    // ── Init ──────────────────────────────────────────────────────────────

    // Initial page load
    document.addEventListener("DOMContentLoaded", () => {
        initExerciseSelects();
        initTagSelect();
        initSortable();
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
                    initSortable();
                    document.body.removeEventListener("htmx:afterSwap", handleAdd);
                }
            });
        }
        // Used afterSettle because with afterSwap default select elements are not hidden properly yet
        if (removeBtn) {
            document.body.addEventListener("htmx:afterSettle", function handleRemove(e) {
                if (e.detail.target.id === "exercise-wrapper") {
                    initExerciseSelects(e.detail.target);
                    initSortable();
                    triggerExerciseHistoryRefresh();
                    document.body.removeEventListener("htmx:afterSettle", handleRemove);
                }
            });
        }
    });
})();
