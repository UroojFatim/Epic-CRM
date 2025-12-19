/** @odoo-module **/
(function () {
  const SEL = [
    ".o_menu_sections .nav > .nav-item",
    ".o_menu_sections .nav > .o_menu_entry",
    ".o_menu_sections .nav > .o_menu_entry_wrap"
  ].join(",");

  function neutralize(root=document) {
    root.querySelectorAll(SEL).forEach(el => {
      el.style.setProperty("background", "transparent", "important");
      el.style.setProperty("background-color", "transparent", "important");
      el.style.setProperty("box-shadow", "none", "important");
      el.style.setProperty("border", "0", "important");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => neutralize(), { once: true });
  } else {
    neutralize();
  }

  const MO = window.MutationObserver || window.WebKitMutationObserver;
  if (MO) {
    const obs = new MO(muts => {
      for (const m of muts) for (const n of m.addedNodes)
        if (n && n.nodeType === 1) neutralize(n);
    });
    obs.observe(document.body || document.documentElement, { childList: true, subtree: true });
  }
})();
