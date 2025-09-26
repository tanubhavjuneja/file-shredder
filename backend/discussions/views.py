from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Discussion
from .serializers import DiscussionSerializer

@api_view(['GET'])
def list_discussions(request):
    discussions = Discussion.objects.all().order_by('-id')
    serializer = DiscussionSerializer(discussions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_discussion(request):
    serializer = DiscussionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)
