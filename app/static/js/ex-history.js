// ----- Update exercise history on client change -----
document.addEventListener("change", function (e) {
  if (e.target && e.target.name === "client") {
    document
      .querySelectorAll('select[name^="exercises-"][name$="-exercise"]')
      .forEach((sel) => {
        if (sel.value && sel.value !== "0") {
          sel.dispatchEvent(new Event("change", { bubbles: true }));
        }
      });
  }
});