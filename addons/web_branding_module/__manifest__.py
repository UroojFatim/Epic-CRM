{
    "name": "Web Theme Custom",
    "version": "17.0.1.0.0",
    "category": "Customization",
    "summary": "Custom Theme Colors for Odoo Backend",
    "depends": ["base", "web"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "web_theme_custom/static/src/css/theme.scss",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
