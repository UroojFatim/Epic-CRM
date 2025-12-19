/** @odoo-module **/
// Safe favicon + theme-color injection for all pages (login, backend, portal)
(function () {
    function ensureMeta(name, content) {
        const el = document.querySelector(`meta[name="${name}"]`);
        if (el) {
            el.setAttribute("content", content);
        } else {
            const m = document.createElement("meta");
            m.setAttribute("name", name);
            m.setAttribute("content", content);
            document.head.appendChild(m);
        }
    }
    function ensureFavicon(href) {
        // prefer explicit rel=icon first
        let link = document.querySelector('link[rel="icon"]');
        if (!link) {
            link = document.createElement("link");
            link.setAttribute("rel", "icon");
            link.setAttribute("type", "image/x-icon");
            document.head.appendChild(link);
        }
        link.setAttribute("href", href);
    }
    if (document && document.head) {
        ensureFavicon("/wolf_debranding/static/src/img/favicon.ico");
        ensureMeta("theme-color", "#000000");
    }
})();
