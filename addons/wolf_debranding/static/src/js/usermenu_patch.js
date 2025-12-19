/** @odoo-module **/
import { registry } from "@web/core/registry";
import { UserMenu } from "@web/webclient/user_menu/user_menu";
import { patch } from "@web/core/utils/patch";

/* Remove Odoo-branded entries from the user menu */
const items = registry.category("user_menuitems");
patch(UserMenu.prototype, {
    setup() {
        super.setup();
        ["documentation", "support", "odoo_account", "about"].forEach(id => { try { items.remove(id); } catch(e){} });
    },
});
