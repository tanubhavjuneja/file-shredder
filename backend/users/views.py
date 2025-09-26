from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import UserProfile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
User = get_user_model()
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    data = {
        "username": user.username,
        "email": user.email,
        "phone": getattr(user, "phone", "")
    }
    return Response(data)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name', '')
    phone = data.get('phone', '')
    if UserProfile.objects.filter(username=username).exists():
        return Response({'success': False, 'message': 'Username already exists'})
    if UserProfile.objects.filter(email=email).exists():
        return Response({'success': False, 'message': 'Email already exists'})
    user = UserProfile.objects.create_user(
        username=username,
        email=email,
        password=password,
        full_name=full_name,
        phone=phone
    )
    token, created = Token.objects.get_or_create(user=user)
    return Response({'success': True, 'token': token.key, 'message': 'User registered successfully'})
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'success': True,
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'full_name': getattr(user, 'full_name', ''),
            'phone': getattr(user, 'phone', ''),
            'message': 'Login successful'
        })
    else:
        return Response({'success': False, 'message': 'Invalid credentials'}, status=401)