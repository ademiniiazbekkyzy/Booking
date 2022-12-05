from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import ElementViewSet, Favourite, ReservationView, ReservationHistory
# from applications.review.views import Review, DetailReview

router = DefaultRouter()
router.register(r'product', ElementViewSet)

urlpatterns = [
    # path('auth/', include('rest_framework_social_oauth2.urls')),
    # path('review/', Review.as_view()),
    path('reserv/', ReservationView.as_view()),
    path('reserv-history/', ReservationHistory.as_view()),
    # path('detail/<int:pk>/', DetailReview.as_view()),
    path('favourite/', Favourite.as_view()),
    # path('parser/', create_hotel_view),
    path('', include(router.urls), name='router'),
    # path('favourite-history/', ),
]