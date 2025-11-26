from django.shortcuts import render

# backend/api/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def contact_form(request):
    """
    Receives contact form data from the React frontend.
    """
    data = request.data
    print("Received message:", data)  # This will print to your terminal console

    # TODO: Add logic here to save to DB or send an email

    return Response({"status": "sent", "message": "Message received!"}, status=status.HTTP_200_OK)
