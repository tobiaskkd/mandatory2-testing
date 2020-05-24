from django.urls import include, path
from greenhouse_keeper_api import views

urlpatterns = [
    path('listAll', views.MeasurementList.as_view()),
    path('', views.MeasurementLogic.as_view())
]
