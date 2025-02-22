from django.shortcuts import render

# Create your views here.
# phishing_backend/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class AccessPageView(APIView):
    def get(self, request):


        return Response({"message": "Welcome to the page!"}, status=status.HTTP_200_OK)
