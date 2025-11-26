from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import ContactMessage
from django.conf import settings


@api_view(['POST'])
def contact_form(request):
    """
    Saves contact form data to the DB and sends an auto-reply email.
    """
    data = request.data

    # Required fields validation
    required = ["name", "email", "message"]
    for field in required:
        if field not in data:
            return Response(
                {"error": f"Missing field: {field}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Save to database
    saved_msg = ContactMessage.objects.create(
        name=data["name"],
        email=data["email"],
        message=data["message"]
    )

    # Send auto-reply email
    try:
        send_mail(
            subject="We received your message!",
            message=(
                f"Hi {data['name']},\n\n"
                "Thank you for contacting us. "
                "Your message has been received and our team will get back to you shortly.\n\n"
                "Best regards,\nYour Company Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[data["email"]],
            fail_silently=False,
        )
    except Exception as e:
        print("Email send error:", e)

    return Response(
        {
            "status": "success",
            "message": "Message saved and email sent!",
            "id": saved_msg.id
        },
        status=status.HTTP_201_CREATED
    )

