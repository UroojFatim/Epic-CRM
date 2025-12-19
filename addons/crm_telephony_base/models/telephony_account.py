# -*- coding: utf-8 -*-
import secrets
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class TelephonyAccount(models.Model):
    _name = "telephony.account"
    _description = "Telephony Account (per tenant/company)"

    name = fields.Char(required=True)
    company_id = fields.Many2one("res.company", required=True, ondelete="cascade")
    provider = fields.Selection(
        [("twilio", "Twilio")],
        required=True, default="twilio"
    )

    # Provider credentials (store encrypted via Odoo fields)
    account_sid = fields.Char(string="Provider Account SID")
    auth_token = fields.Char(string="Provider Auth Token")
    default_sms_from = fields.Char(string="Default SMS From (E.164)")
    default_voice_from = fields.Char(string="Default Voice From (E.164)")

    # Public base URL (e.g., your ngrok/prod domain). We use it to build callback URLs.
    public_base_url = fields.Char(string="Public Base URL")

    # Tenant token for webhook routing
    tenant_token = fields.Char(readonly=True, copy=False)

    # Bot toggles
    bot_on_inbound = fields.Boolean(default=False)
    bot_on_outbound = fields.Boolean(default=False)

    # Optional: route all inbound to a fallback agent number if bot disabled
    default_agent_number = fields.Char(string="Default Agent Number")

    dry_run = fields.Boolean(default=True, help="Simulate without hitting provider")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("tenant_token"):
                vals["tenant_token"] = secrets.token_urlsafe(24)
        return super().create(vals_list)

    def _ensure_ready(self):
        for rec in self:
            if rec.dry_run:
                continue
            if not (rec.account_sid and rec.auth_token):
                raise UserError(_("Telephony credentials are not set."))
            if not rec.public_base_url:
                raise UserError(_("Public Base URL is required (ngrok/prod)."))
