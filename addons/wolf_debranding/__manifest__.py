{
    "name": "WolfOfArchesCRM – Debrand/Theme",
    "summary": "Complete debranding of Odoo CE 17: rename to WolfOfArchesCRM, black background, red accents, white text.",
    "version": "17.0.2.27",  # bump so assets rebuild
    "author": "Wolf of Arches",
    "license": "LGPL-3",
    "depends": ["web", "base", "mail", "website"],
    "assets": {
# compile-time variable overrides (this is what kills baked-in purple)
        "web._assets_primary_variables": [
            "wolf_debranding/static/src/scss/variables.scss",
        ],


        "web.assets_backend": [
            "wolf_debranding/static/src/scss/backend.scss",
            "wolf_debranding/static/src/scss/nav_fix_all.scss",
            "wolf_debranding/static/src/js/nav_wrapper_transparent.js",
             "wolf_debranding/static/src/js/nav_bar_vars.js",
   
            
            "wolf_debranding/static/src/js/title_patch.js",
            "wolf_debranding/static/src/js/usermenu_patch.js",          # <-- match your filename
            "wolf_debranding/static/src/js/favicon_inject.js",
            "wolf_debranding/static/src/js/settings_hide_sections.js",
            "wolf_debranding/static/src/js/settings_cleanup.js",
            "wolf_debranding/static/src/js/settings_rebrand_text.js",
            "wolf_debranding/static/src/js/nav_bar_vars.js"
            "wolf_debranding/static/src/js/force_brand_vars.js",
            
        ],  

        "web.assets_frontend": [
            "wolf_debranding/static/src/scss/frontend.scss",
            "wolf_debranding/static/src/scss/website_palette.scss",
            "wolf_debranding/static/src/js/favicon_inject.js",
            # "wolf_debranding/static/src/js/settings_cleanup.js",
            # "wolf_debranding/static/src/js/settings_rebrand_text.js",
        ],
    },
    "data": [
        "views/qweb.xml",
        "views/website.xml",
        "views/email.xml",
    ],
}
