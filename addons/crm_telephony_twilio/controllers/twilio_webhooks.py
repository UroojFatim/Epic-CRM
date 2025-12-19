# -*- coding: utf-8 -*-
import base64
import hmac
import hashlib
import logging
from urllib.parse import urlparse, parse_qsl
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

def _find_account_by_token(token):
    return request.env["telephony.account"].sudo().search([("tenant_token", "=", token)], limit=1)

def _validate_twilio_signature(req, full_url, auth_token):
    """
    Twilio sends X-Twilio-Signature; we must compute HMAC-SHA1 of the URL + sorted params.
    See: https://www.twilio.com/docs/usage/security#validating-requests
    """
    signature = req.headers.get("X-Twilio-Signature")
    if not signature:
        return False
    # Raw body form parameters (Twilio posts application/x-www-form-urlencoded)
    body = req.httprequest.form
    # Build the string: URL (without query) + concatenated sorted params
    u = urlparse(full_url)
    url_without_query = f"{u.scheme}://{u.netloc}{u.path}"
    params = sorted(body.items(), key=lambda x: x[0])
    data = url_without_query + "".join([k + v for k, v in params])
    mac = hmac.new(auth_token.encode("utf-8"), data.encode("utf-8"), hashlib.sha1)
    digest = base64.b64encode(mac.digest()).decode("utf-8")
    return hmac.compare_digest(digest, signature)

class TwilioWebhooks(http.Controller):

    @http.route(['/t/<string:tenant>/twilio/sms/status'], type='http', auth='public', csrf=False, methods=['POST'])
    def sms_status(self, tenant, **kwargs):
        account = _find_account_by_token(tenant)
        if not account:
            return request.make_response("tenant not found", headers=[('Content-Type', 'text/plain')], status=404)

        if not account.dry_run:
            full_url = request.httprequest.url
            if not _validate_twilio_signature(request, full_url, account.auth_token or ""):
                _logger.warning("Twilio signature invalid (SMS status) for tenant %s", tenant)
                return request.make_response("invalid signature", headers=[('Content-Type', 'text/plain')], status=403)

        sid = kwargs.get("MessageSid")
        status = kwargs.get("MessageStatus")
        price = kwargs.get("Price")
        price_unit = kwargs.get("PriceUnit")
        msg = request.env["telephony.message"].sudo().search([("provider_sid", "=", sid)], limit=1)
        if msg:
            msg.write({
                "status": status,
                "price": float(price or 0),
                "price_unit": price_unit or msg.price_unit,
            })
        return request.make_response("ok", headers=[('Content-Type', 'text/plain')])

    @http.route(['/t/<string:tenant>/twilio/voice/status'], type='http', auth='public', csrf=False, methods=['POST'])
    def voice_status(self, tenant, **kwargs):
        account = _find_account_by_token(tenant)
        if not account:
            return request.make_response("tenant not found", headers=[('Content-Type', 'text/plain')], status=404)

        if not account.dry_run:
            full_url = request.httprequest.url
            if not _validate_twilio_signature(request, full_url, account.auth_token or ""):
                _logger.warning("Twilio signature invalid (Voice status) for tenant %s", tenant)
                return request.make_response("invalid signature", headers=[('Content-Type', 'text/plain')], status=403)

        sid = kwargs.get("CallSid")
        call_status = kwargs.get("CallStatus")
        duration = int(kwargs.get("CallDuration") or 0)
        price = kwargs.get("CallPrice") or kwargs.get("Price")
        price_unit = kwargs.get("PriceUnit")
        rec = request.env["telephony.call"].sudo().search([("provider_sid", "=", sid)], limit=1)
        if rec:
            rec.write({
                "status": call_status,
                "duration_sec": duration,
                "price": float(price or 0),
                "price_unit": price_unit or rec.price_unit,
            })
        return request.make_response("ok", headers=[('Content-Type', 'text/plain')])

    @http.route(['/t/<string:tenant>/twilio/voice/inbound'], type='http', auth='public', csrf=False, methods=['POST', 'GET'])
    def voice_inbound(self, tenant, **kwargs):
        """
        Returns TwiML based on bot toggle.
        - If ?human=1 or bot disabled -> Dial agent
        - Else -> connect to bot via <Connect><Stream> (you can replace with your own gateway)
        """
        account = _find_account_by_token(tenant)
        if not account:
            return request.make_response("tenant not found", headers=[('Content-Type', 'text/plain')], status=404)

        # Signature validation for POST; Twilio may request via GET for Url fetch; validate only when token present
        if request.httprequest.method == "POST" and not account.dry_run:
            full_url = request.httprequest.url
            if not _validate_twilio_signature(request, full_url, account.auth_token or ""):
                _logger.warning("Twilio signature invalid (Voice inbound) for tenant %s", tenant)
                return request.make_response("invalid signature", headers=[('Content-Type', 'text/plain')], status=403)

        to = kwargs.get("To")  # our Twilio number
        frm = kwargs.get("From")  # caller/lead
        human_only = request.httprequest.args.get("human") == "1"
        use_bot = account.bot_on_inbound and not human_only

        # Try to map to a lead if we can (optional)
        Lead = request.env["crm.lead"].sudo()
        lead = Lead.search([("mobile", "=", frm)], limit=1) or Lead.search([("phone", "=", frm)], limit=1)

        if use_bot:
            # Replace with your websocket media stream if you have one
            # For MVP: simple prompt + hangup so flows are wired
            xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say>Hi, thanks for calling {request.env.company.name}. Our assistant will help you now.</Say>
  <Pause length="1"/>
  <Say>We are currently in demo mode. An agent will contact you shortly. Goodbye.</Say>
  <Hangup/>
</Response>"""
        else:
            agent = account.default_agent_number or (request.env.company.phone or "")
            if not agent:
                xml = """<?xml version="1.0" encoding="UTF-8"?><Response><Say>No agent configured. Goodbye.</Say><Hangup/></Response>"""
            else:
                xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say>Connecting you to an agent.</Say>
  <Dial timeout="25">{agent}</Dial>
</Response>"""

        headers = [('Content-Type', 'text/xml')]
        # Log inbound call record quickly (if not already created on outbound leg)
        call = request.env["telephony.call"].sudo().search([("provider_sid", "=", kwargs.get("CallSid"))], limit=1)
        if not call:
            request.env["telephony.call"].sudo().create({
                "account_id": account.id, "lead_id": lead.id if lead else False,
                "direction": "in", "frm": frm, "to": to, "provider": "twilio",
                "provider_sid": kwargs.get("CallSid"), "status": "inbound"
            })
        return request.make_response(xml, headers=headers)
