from rest_framework import serializers
from .models import NewsFlash

class NewsFlashSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsFlash
        fields = '__all__'
