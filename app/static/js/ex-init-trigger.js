// ----- Trigger change events on pre-filled exercise selects to load history -----
function triggerExerciseHistoryRefresh() {
  document
    .querySelectorAll('select[name^="exercises-"][name$="-exercise"]')
    .forEach(function (sel) {
      if (sel.value && sel.value !== "0") {
        // Use htmx.trigger for TomSelect-wrapped selects
        htmx.trigger(sel, "change");
      }
    });
}

document.addEventListener("DOMContentLoaded", triggerExerciseHistoryRefresh);

// ----- Refresh history after exercise row is removed -----
document.addEventListener("htmx:afterSettle", function (e) {
  if (e.detail.target && e.detail.target.id === "exercise-wrapper") {
    triggerExerciseHistoryRefresh();
  }
});
