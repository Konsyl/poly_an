from django.urls import path
from polygon_rest import views

urlpatterns = [
    path('', views.is_ok.as_view()),
    path('dots/', views.DotController.as_view()),
    path('dotsfromR/', views.DotController.as_view())

]