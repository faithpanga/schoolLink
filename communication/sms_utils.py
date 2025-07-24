from twilio.rest import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_sms(to_number, body):
    """
    Sends an SMS using Twilio credentials stored in settings.
    Returns True on success, False on failure.
    """
    # Check if Twilio is configured before attempting to send
    if not all(
        [
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
            settings.TWILIO_PHONE_NUMBER,
        ]
    ):
        logger.warning("Twilio settings are not configured. SMS not sent.")
        return False

    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=body, from_=settings.TWILIO_PHONE_NUMBER, to=str(to_number)
        )
        logger.info(f"SMS sent successfully to {to_number}")
        return True
    except Exception as e:
        # Catch any exception from the Twilio API (e.g., invalid number, network error)
        logger.error(f"Error sending SMS to {to_number}: {e}")
        return False
