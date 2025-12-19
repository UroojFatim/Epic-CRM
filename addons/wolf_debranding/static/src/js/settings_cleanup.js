/** @odoo-module **/
// Hide "Odoo XX.X" / vendor / license lines + doc/help links/icons in Settings.
// Defensive: don't observe until DOM is ready; never throw.

(function () {
    const MATCHERS = [
        /Odoo\s*\d+\.\d+/i,   // "Odoo 17.0", etc.
        /Odoo\s+S\.?A\.?/i,   // "Odoo S.A."
        /GNU\s+LGPL/i,
        /Community\s+Edition/i,
        /Enterprise\s+Edition/i,
    ];

    function shouldHide(el) {
        const t = (el.innerText || el.textContent || "").replace(/\s+/g, " ").trim();
        return t && MATCHERS.some((re) => re.test(t));
    }

    function cleanup(root = document) {
        try {
            const scope =
                root.querySelector(".o_settings_container") ||
                root.querySelector(".o_form_view") ||
                root;

            // version/vendor/license lines
            scope.querySelectorAll("small, p, div, span").forEach((el) => {
                if (el.__woaHidden) return;
                if (shouldHide(el)) {
                    (el.closest("small, p, div, span") || el).style.display = "none";
                    el.__woaHidden = true;
                }
            });

            // doc/help links & question icons
            scope.querySelectorAll([
                'a[href*="odoo.com"]',
                'a[href*="odoo.sh"]',
                'a[href*="odoo.saas"]',
                'a.o_doc_link', '.o_doc_link',
                '.fa-question-circle', '.fa-question-circle-o',
                '[title*="Documentation"]',
                '[data-oe-help-url]',
            ].join(",")).forEach((node) => {
                const wrap = node.closest("small, p, div, span, a") || node;
                wrap.style.display = "none";
            });
        } catch (e) {
            // never break the SPA
            console.warn("wolf_debranding settings cleanup skipped:", e);
        }
    }

    function start() {
        cleanup(document);
        const MO = window.MutationObserver || window.WebKitMutationObserver;
        if (!MO) return;
        const target = document.documentElement || document.body;
        if (!target) return;  // ultra-defensive

        const obs = new MO((mut) => {
            for (const m of mut) {
                for (const n of m.addedNodes) {
                    if (n && n.nodeType === 1) cleanup(n);
                }
            }
        });
        obs.observe(target, { childList: true, subtree: true });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start, { once: true });
    } else {
        start();
    }
})();
