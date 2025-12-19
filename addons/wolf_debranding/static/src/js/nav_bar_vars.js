/** @odoo-module **/
(function () {
  const scope = document.querySelector('.o_main_navbar .o_menu_sections');
  function pinVars(el){
    if (!el) return;
    el.style.setProperty('--NavBar-entry-backgroundColor', 'transparent', 'important');
    el.style.setProperty('--NavBar-entry-hover-backgroundColor', 'transparent', 'important');
    el.style.setProperty('--NavBar-entry-active-backgroundColor', 'transparent', 'important');
    el.style.setProperty('--NavBar-entrySelected-backgroundColor', 'transparent', 'important');
  }
  if (scope) pinVars(scope);
  const MO = window.MutationObserver || window.WebKitMutationObserver;
  if (MO) {
    const obs = new MO(() => pinVars(document.querySelector('.o_main_navbar .o_menu_sections')));
    obs.observe(document.documentElement, { attributes: true, childList: true, subtree: true });
  }
})();
