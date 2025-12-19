# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = "crm.lead"

    last_sms_status = fields.Char(readonly=True)
    last_call_status = fields.Char(readonly=True)
    use_bot_for_this_lead = fields.Boolean(default=False, string="Use Bot")

    def _get_account_for_company(self):
        self.ensure_one()
        account = self.env["telephony.account"].sudo().search(
            [("company_id", "=", self.company_id.id)], limit=1
        )
        if not account:
            raise UserError(_("No Telephony Account configured for %s.") % self.company_id.name)
        return account

    def action_send_sms(self):
        for lead in self:
            account = lead._get_account_for_company()
            to_number = (lead.mobile or lead.phone or "").strip()
            if not to_number:
                raise UserError(_("No phone/mobile on this lead."))
            body = _("Hello %s, this is %s from %s regarding your inquiry.") % (
                lead.contact_name or lead.partner_name or _("there"),
                self.env.user.name,
                self.env.company.name,
            )
            # Delegate to provider adapter (Twilio module registers this method)
            res = self.env["ir.model.data"]._xmlid_to_res_id  # just to ensure module loaded
            provider = self.env["ir.config_parameter"].sudo().get_param("crm_telephony.provider.loaded", "twilio")
            if provider != "twilio":
                raise UserError(_("Only Twilio provider is loaded in this build."))

            status = self.env["twilio.provider"].sudo().send_sms(
                account=account, to=to_number, body=body, lead=lead
            )
            lead.write({"last_sms_status": status})
        return True

    def action_call_lead(self):
        for lead in self:
            account = lead._get_account_for_company()
            to_number = (lead.mobile or lead.phone or "").strip()
            if not to_number:
                raise UserError(_("No phone/mobile on this lead."))

            use_bot = lead.use_bot_for_this_lead or account.bot_on_outbound
            status = self.env["twilio.provider"].sudo().start_call(
                account=account, to=to_number, lead=lead, use_bot=use_bot
            )
            lead.write({"last_call_status": status})
        return True
