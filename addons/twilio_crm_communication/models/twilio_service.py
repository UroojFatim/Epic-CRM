from urllib.parse import quote

from odoo import _, models
from odoo.exceptions import UserError


class TwilioCrmService(models.AbstractModel):
    _name = 'twilio.crm.service'
    _description = 'Twilio CRM Service'

    def _normalize_phone_number(self, number):
        if not number:
            return number
        number = number.strip()
        if number.startswith('+'):
            return number
        return number.replace(' ', '').replace('-', '')

    def _resolve_to_number(self, lead, to_number):
        lead_number = lead.mobile or lead.phone
        if not lead_number and not to_number:
            raise UserError(_('Lead has no phone or mobile number.'))
        return self._normalize_phone_number(to_number or lead_number)

    def _get_config(self):
        params = self.env['ir.config_parameter'].sudo()
        config = {
            'account_sid': params.get_param('twilio_crm.account_sid'),
            'auth_token': params.get_param('twilio_crm.auth_token'),
            'from_number': self._normalize_phone_number(params.get_param('twilio_crm.from_number')),
            'webhook_base_url': (params.get_param('twilio_crm.webhook_base_url') or '').strip(),
            'twiml_app_sid': params.get_param('twilio_crm.twiml_app_sid'),
        }

        required = {
            'account_sid': _('Twilio Account SID'),
            'auth_token': _('Twilio Auth Token'),
            'from_number': _('Twilio From Number'),
            'webhook_base_url': _('Twilio Webhook Base URL'),
        }
        missing = [label for key, label in required.items() if not config.get(key)]
        if missing:
            raise UserError(
                _('Missing Twilio configuration values: %s') % ', '.join(missing)
            )
        return config

    def _get_client(self):
        config = self._get_config()
        try:
            from twilio.rest import Client
        except ImportError as error:
            raise UserError(_('Twilio Python SDK is not installed.')) from error
        return Client(config['account_sid'], config['auth_token'])

    def send_sms(self, lead, to_number, body):
        config = self._get_config()
        client = self._get_client()

        to_number = self._resolve_to_number(lead, to_number)
        message = client.messages.create(
            from_=config['from_number'],
            to=to_number,
            body=body,
        )

        self.env['twilio.sms.log'].create({
            'lead_id': lead.id,
            'partner_id': lead.partner_id.id,
            'to_number': to_number,
            'from_number': config['from_number'],
            'body': body,
            'twilio_sid': message.sid,
            'status': getattr(message, 'status', False),
        })
        return message.sid

    def make_call(self, lead, to_number):
        config = self._get_config()
        client = self._get_client()

        to_number = self._resolve_to_number(lead, to_number)
        from_number = config['from_number']
        twiml_app_sid = (config.get('twiml_app_sid') or '').strip()

        if twiml_app_sid:
            call = client.calls.create(
                to=to_number,
                from_=from_number,
                application_sid=twiml_app_sid,
            )
        else:
            webhook_base_url = config['webhook_base_url'].rstrip('/')
            url = f"{webhook_base_url}/twilio/voice/twiml?to={quote(to_number, safe='')}"
            call = client.calls.create(
                to=to_number,
                from_=from_number,
                url=url,
            )

        self.env['twilio.call.log'].create({
            'lead_id': lead.id,
            'to_number': to_number,
            'from_number': from_number,
            'twilio_sid': call.sid,
            'status': 'queued',
        })
        return call.sid
