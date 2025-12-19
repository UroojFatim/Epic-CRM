/** @odoo-module **/
// Remove the whole "Odoo IAP" and "Progressive Web App" setting boxes.

(function () {
    const TARGET_TITLES = [
        /^Odoo\s+IAP$/i,
        /^Progressive\s+Web\s+App$/i,
    ];

    function closestSettingBox(node) {
        return node.closest?.(".o_setting_container, .o_setting_box, .o_setting") || node.closest?.("section") || null;
    }

    function killBoxes(root=document) {
        const scope = root.querySelector(".o_settings_container, .o_form_view, .o_web_settings") || null;
        if (!scope) return;

        // Titles usually live in .o_setting_left .o_form_label or .o_setting_box h2/h3/label
        scope.querySelectorAll(".o_setting_box, .o_setting").forEach(box => {
            const titleEl = box.querySelector("label, h2, h3, .o_form_label, .o_setting_left label");
            const title = (titleEl?.textContent || "").trim();
            if (title && TARGET_TITLES.some(re => re.test(title))) {
                box.style.display = "none";
            }
        });
    }

    function start() {
        killBoxes(document);
        const MO = window.MutationObserver || window.WebKitMutationObserver;
        if (!MO) return;
        const obs = new MO(muts => {
            for (const m of muts) for (const n of m.addedNodes) if (n && n.nodeType === 1) killBoxes(n);
        });
        obs.observe(document.body || document.documentElement, { childList: true, subtree: true });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start, { once: true });
    } else {
        start();
    }
})();
