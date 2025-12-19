/** @odoo-module **/
(function () {
  function setVars(root) {
    const s = (k, v) => root.style.setProperty(k, v, "important");
    s("--o-brand-odoo", "#D0021B");
    s("--o-brand-primary", "#D0021B");
    s("--bs-primary", "#D0021B");
    s("--o-brand-odoo-rgb", "208, 2, 27");
    s("--o-brand-primary-rgb", "208, 2, 27");
    s("--bs-primary-rgb", "208, 2, 27");
  }
  const r = document.documentElement;
  if (r) setVars(r);

  const MO = window.MutationObserver || window.WebKitMutationObserver;
  if (!MO) return;
  const obs = new MO(() => setVars(document.documentElement));
  obs.observe(document.documentElement, { attributes: true, attributeFilter: ["style", "class"] });
})();
