from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import *
# from applications.review.views import Review, DetailReview

router = DefaultRouter()
router.register("booking", EntryViewSet)
# router.register("comments", CommentViewSet)

urlpatterns = [
    # path('comment/', Comment.as_view()),
    # path('reserv/', ReservationView.as_view()),
    path('reserv-history/', ReservationHistory.as_view()),
    path('review/', Review.as_view()),
    # path('detail/<int:pk>/', DetailReview.as_view()),
    path('elements/', ElementAPIList.as_view()),
    path('element/<int:pk>/', ElementAPIUpdate.as_view()),
    path('element/<int:pk>/', ElementDestroy.as_view()),
    # path('book/', BookingCreateApiView.as_view(), name='book_room'),
    # path('comments/', CommentListCreateView.as_view()),
    # path('comments/<int:pk>/', CommentDetailView.as_view()),
    path('', include(router.urls), name='router'),
]
