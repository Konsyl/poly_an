from asgiref.sync import async_to_sync
from django.urls import path
from polygon_rest import views


urlpatterns = [
    path('', views.IsOk.as_view()),
    path('dots/', views.DotsController.as_view()),
    path('dotfromR/', views.DotController.as_view()),
    path('dot/<int:pk>', views.DotController.as_view()),
]
