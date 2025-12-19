/** @odoo-module **/
import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

/* Replace leading app title from "Odoo" to "WolfOfArchesCRM" */
patch(WebClient.prototype, {
    setup() {
        super.setup();
        const titleService = useService("title");
        titleService.setParts({ zopenerp: "WolfOfArchesCRM" });
    },
});
