"""booking_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter

from main.views import PostViewSet, CategoryListView

schema_view = get_schema_view(
    openapi.Info(
        title='Booking project',
        description='Бронь fields',
        default_version='v1',
    ),
    public=True
)
router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('account/', include('account.urls')),
    path('v1/api/', include(router.urls)),
    path('v1/api/categories/', CategoryListView.as_view()),
    # path('v1/api/', include('main.urls')),
    path('swagger/', schema_view.with_ui('swagger')),
]
