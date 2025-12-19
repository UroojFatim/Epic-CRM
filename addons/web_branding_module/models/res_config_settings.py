from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    web_theme_primary = fields.Char(
        string="Primary Color",
        config_parameter="web_theme_custom.primary",
        default="#2b90d9"
    )
    web_theme_secondary = fields.Char(
        string="Secondary Color",
        config_parameter="web_theme_custom.secondary",
        default="#ffffff"
    )
    web_theme_accent = fields.Char(
        string="Accent Color",
        config_parameter="web_theme_custom.accent",
        default="#ff7b7b"
    )
    web_theme_header_bg = fields.Char(
        string="Header Background",
        config_parameter="web_theme_custom.header_bg",
        default="#2b90d9"
    )
    web_theme_mode = fields.Selection(
        [
            ("light", "Light"),
            ("dark", "Dark"),
        ],
        string="Theme Mode",
        config_parameter="web_theme_custom.theme",
        default="light"
    )
