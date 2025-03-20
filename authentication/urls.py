from django.urls import path

from authentication.views import RegisterView, LoginView, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/', VerifyEmailView.as_view(), name='login'),

]