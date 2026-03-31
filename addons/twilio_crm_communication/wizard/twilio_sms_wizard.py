from odoo import _, fields, models
from odoo.exceptions import UserError


class TwilioSmsWizard(models.TransientModel):
    _name = 'twilio.sms.wizard'
    _description = 'Twilio SMS Wizard'

    lead_id = fields.Many2one('crm.lead', required=True)
    to_number = fields.Char(required=True)
    body = fields.Text(required=True)

    def action_send_sms(self):
        self.ensure_one()
        if not (self.body or '').strip():
            raise UserError(_('SMS body cannot be empty.'))

        sid = self.env['twilio.crm.service'].send_sms(
            self.lead_id,
            self.to_number,
            self.body,
        )
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Twilio SMS'),
                'message': _('SMS sent (SID: %s)') % sid,
                'type': 'success',
                'sticky': False,
            },
        }
