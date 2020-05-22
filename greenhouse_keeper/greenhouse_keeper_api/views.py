from django.contrib.auth.models import User, Group
from .models import Measurement
from rest_framework import viewsets
from rest_framework import permissions
from greenhouse_keeper_api.serializers import UserSerializer, GroupSerializer, MeasurementSerializer
from rest_framework import generics


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


class MeasurementList(generics.ListCreateAPIView):
    """
    API endpoint that returns a list of all measurements.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]


'''
class MeasurementCreate(generics.CreateAPIView):
    """
    API endpoint that allows measurements to be created.
    """
    queryset = Measurement.objects.create()
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]
'''
