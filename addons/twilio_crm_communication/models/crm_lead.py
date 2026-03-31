from odoo import _, models
from odoo.exceptions import AccessError, UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _twilio_check_access(self):
        if not self.env.user.has_group('twilio_crm_communication.group_twilio_user'):
            raise AccessError(_('You are not allowed to use Twilio actions.'))

    def _twilio_get_phone(self):
        self.ensure_one()
        number = self.phone or self.mobile
        if not number:
            raise UserError(_('This lead has no phone or mobile number.'))
        return number

    def action_twilio_call(self):
        self.ensure_one()
        self._twilio_check_access()

        number = self._twilio_get_phone()
        sid = self.env['twilio.crm.service'].make_call(self, number)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Twilio Call Started'),
                'message': _('Call SID: %s') % sid,
                'type': 'success',
                'sticky': False,
            },
        }

    def action_twilio_sms(self):
        self.ensure_one()
        self._twilio_check_access()

        to_number = self._twilio_get_phone()
        body = _('Hi %s,') % (self.partner_name or self.name or _('there'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Send SMS'),
            'res_model': 'twilio.sms.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_lead_id': self.id,
                'default_to_number': to_number,
                'default_body': body,
            },
        }
