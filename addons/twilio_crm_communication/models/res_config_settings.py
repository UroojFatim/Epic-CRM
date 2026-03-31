from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    twilio_account_sid = fields.Char(
        string='Twilio Account SID',
        config_parameter='twilio_crm.account_sid',
        help='Twilio Account SID used to authenticate API calls.',
    )
    twilio_auth_token = fields.Char(
        string='Twilio Auth Token',
        config_parameter='twilio_crm.auth_token',
        password=True,
        help='Twilio Auth Token paired with the Account SID.',
    )
    twilio_from_number = fields.Char(
        string='Twilio From Number',
        config_parameter='twilio_crm.from_number',
        help='Default Twilio phone number in E.164 format (e.g. +14155552671).',
    )
    twilio_webhook_base_url = fields.Char(
        string='Twilio Webhook Base URL',
        config_parameter='twilio_crm.webhook_base_url',
        help='Public HTTPS base URL used by Twilio to call webhook endpoints.',
    )
    twilio_twiml_app_sid = fields.Char(
        string='Twilio TwiML App SID',
        config_parameter='twilio_crm.twiml_app_sid',
        help='Optional TwiML App SID for call routing and behavior.',
    )
