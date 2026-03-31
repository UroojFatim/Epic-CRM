from odoo import fields, models


class TwilioCallLog(models.Model):
    _name = 'twilio.call.log'
    _description = 'Twilio Call Log'
    _order = 'created_at desc'

    name = fields.Char(default='Call')
    lead_id = fields.Many2one('crm.lead')
    to_number = fields.Char()
    from_number = fields.Char()
    twilio_sid = fields.Char(index=True)
    status = fields.Char()
    direction = fields.Selection(
        [('outbound', 'Outbound'), ('inbound', 'Inbound')],
        default='outbound',
    )
    duration = fields.Integer()
    error_message = fields.Text()
    created_by = fields.Many2one('res.users', default=lambda self: self.env.user)
    created_at = fields.Datetime(default=fields.Datetime.now)
