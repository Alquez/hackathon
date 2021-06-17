from django.urls import path

from . import views



urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationView.as_view(), name='activation_code')
]