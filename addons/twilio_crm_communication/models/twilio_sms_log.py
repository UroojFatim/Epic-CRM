from odoo import fields, models


class TwilioSmsLog(models.Model):
    _name = 'twilio.sms.log'
    _description = 'Twilio SMS Log'
    _order = 'sent_at desc'

    name = fields.Char(default='SMS')
    lead_id = fields.Many2one('crm.lead', index=True)
    partner_id = fields.Many2one('res.partner')
    to_number = fields.Char()
    from_number = fields.Char()
    body = fields.Text()
    twilio_sid = fields.Char(index=True)
    status = fields.Char()
    error_message = fields.Text()
    sent_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    sent_at = fields.Datetime(default=fields.Datetime.now)
