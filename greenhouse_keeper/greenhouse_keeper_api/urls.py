from django.urls import include, path
from rest_framework import routers
from greenhouse_keeper_api import views
'''
router = routers.DefaultRouter()
router.register(r'measurement', views.MeasurementViewSet)
'''
urlpatterns = [
    path('', views.MeasurementList.as_view()),
    path('logic', views.MeasurementLogic.as_view())
]
