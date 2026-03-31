from xml.sax.saxutils import escape

from odoo import http
from odoo.http import request


class TwilioWebhooksController(http.Controller):

    @http.route('/twilio/voice/twiml', type='http', auth='public', methods=['GET'], csrf=False)
    def twilio_voice_twiml(self, **kwargs):
        to_number = (kwargs.get('to') or '').strip()
        twiml = f'<Response><Dial>{escape(to_number)}</Dial></Response>'
        return request.make_response(
            twiml,
            headers=[('Content-Type', 'text/xml; charset=utf-8')],
        )

    @http.route('/twilio/voice/status', type='http', auth='public', methods=['POST'], csrf=False)
    def twilio_voice_status(self, **kwargs):
        call_sid = (kwargs.get('CallSid') or '').strip()
        call_status = (kwargs.get('CallStatus') or '').strip()
        to_number = (kwargs.get('To') or '').strip()
        from_number = (kwargs.get('From') or '').strip()
        call_duration_raw = (kwargs.get('CallDuration') or '').strip()

        values = {
            'status': call_status,
            'to_number': to_number,
            'from_number': from_number,
        }
        if call_duration_raw.isdigit():
            values['duration'] = int(call_duration_raw)

        call_log_model = request.env['twilio.call.log'].sudo()
        if call_sid:
            call_log = call_log_model.search([('twilio_sid', '=', call_sid)], limit=1)
            values['twilio_sid'] = call_sid
            if call_log:
                call_log.write(values)
            else:
                call_log_model.create(values)

        return request.make_response(
            'OK',
            headers=[('Content-Type', 'text/plain; charset=utf-8')],
        )
