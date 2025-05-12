from django.shortcuts import render
from rest_framework import viewsets
from .models import NewsFlash
from .serializers import NewsFlashSerializer

# Create your views here.

class NewsFlashViewSet(viewsets.ModelViewSet):
    queryset = NewsFlash.objects.all().order_by('-date')
    serializer_class = NewsFlashSerializer
