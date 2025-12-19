# -*- coding: utf-8 -*-
from odoo import models, fields

class TelephonyCall(models.Model):
    _name = "telephony.call"
    _description = "Call Detail Record (CDR)"
    _order = "id desc"

    account_id = fields.Many2one("telephony.account", required=True, ondelete="restrict")
    lead_id = fields.Many2one("crm.lead", ondelete="set null")
    direction = fields.Selection([("out", "Outbound"), ("in", "Inbound")], required=True)
    frm = fields.Char(string="From")
    to = fields.Char(string="To")
    provider = fields.Char()
    provider_sid = fields.Char()
    status = fields.Char()
    duration_sec = fields.Integer()
    price = fields.Float()
    price_unit = fields.Char()
    recording_url = fields.Char()
    transcript = fields.Text()
    intent = fields.Char()
    disposition = fields.Selection([
        ("connected", "Connected"),
        ("no_answer", "No Answer"),
        ("busy", "Busy"),
        ("failed", "Failed"),
        ("transferred", "Transferred"),
        ("voicemail", "Voicemail"),
    ])
