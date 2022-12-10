from django.urls import path
from account.views import *

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('custom/', CustomView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ForgotCompletePasswordApiView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]
