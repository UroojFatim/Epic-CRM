# -*- coding: utf-8 -*-
from odoo import models, fields

class TelephonyMessage(models.Model):
    _name = "telephony.message"
    _description = "SMS Log"
    _order = "id desc"

    account_id = fields.Many2one("telephony.account", required=True, ondelete="restrict")
    lead_id = fields.Many2one("crm.lead", ondelete="set null")
    direction = fields.Selection([("out", "Outbound"), ("in", "Inbound")], required=True)
    frm = fields.Char(string="From")
    to = fields.Char(string="To")
    body = fields.Text()
    provider = fields.Char()
    provider_sid = fields.Char()
    status = fields.Char()
    price = fields.Float()
    price_unit = fields.Char()
    error = fields.Char()
