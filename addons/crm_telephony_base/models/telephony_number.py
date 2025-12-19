# -*- coding: utf-8 -*-
from odoo import models, fields

class TelephonyNumber(models.Model):
    _name = "telephony.number"
    _description = "Telephony Numbers"

    name = fields.Char()
    account_id = fields.Many2one("telephony.account", required=True, ondelete="cascade")
    phone_e164 = fields.Char(required=True)
    can_sms = fields.Boolean(default=True)
    can_voice = fields.Boolean(default=True)
    route_to_agent = fields.Char(
        help="Optional fixed route for inbound when bot disabled (e.g., +15551234567). "
             "If empty, uses account.default_agent_number."
    )
    notes = fields.Text()
