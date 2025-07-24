from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from accounts.models import User
from students.models import Student
from communication.models import Message
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def sms_webhook(request):
    if request.method == "POST":
        parent_phone = request.POST.get("From", "")
        sms_body = request.POST.get("Body", "")

        try:
            parent_user = User.objects.get(phone_number=parent_phone, role="PARENT")
            student = Student.objects.filter(parent=parent_user).first()

            if student:
                Message.objects.create(
                    sender=parent_user,
                    student=student,
                    subject=f"SMS Reply from {parent_user.first_name}",
                    body=sms_body,
                    source=Message.Source.SMS,
                )
                logger.info(
                    f"SMS from {parent_phone} successfully processed and logged for student {student.id}."
                )
            else:
                logger.warning(
                    f"SMS received from parent {parent_phone} who has no students."
                )
        except User.DoesNotExist:
            logger.warning(f"SMS received from unknown number: {parent_phone}")

        # Respond to Twilio to acknowledge receipt
        response = MessagingResponse()
        return HttpResponse(str(response), content_type="application/xml")

    return HttpResponse("This endpoint is for Twilio webhooks only.", status=405)
