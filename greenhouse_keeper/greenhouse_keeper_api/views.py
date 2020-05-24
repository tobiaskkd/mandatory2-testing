from django.contrib.auth.models import User, Group
from .models import Measurement
from rest_framework import viewsets
from rest_framework import permissions
from greenhouse_keeper_api.serializers import UserSerializer, GroupSerializer, MeasurementSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import json
from .measurement_helper import Measurement_helper


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasurementLogic(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        measurement = Measurement.objects.filter(created_by=request.user).latest('time')
        serializer = MeasurementSerializer(measurement)
        measurement_helper = Measurement_helper(serializer.data)
        return Response(measurement_helper.get_data())

    def post(self, request, format=None):
        serializer = MeasurementSerializer(data=request.data)
        if serializer.is_valid():
            # Processes the data
            measurement_helper = Measurement_helper(serializer.validated_data)
            serializer.save(created_by=request.user, message=measurement_helper.message)
            return Response(measurement_helper.get_data(), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeasurementList(generics.ListCreateAPIView):
    """
    API endpoint that returns a list of all measurements.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
