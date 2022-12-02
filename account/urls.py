from django.urls import path

from account.views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<uuid:activation_code>/', ActivateView.as_view()),  # /<uuid:activation_code>
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
