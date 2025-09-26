from rest_framework import serializers
from .models import Discussion

class DiscussionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Discussion
        fields = ['id', 'title', 'user']
