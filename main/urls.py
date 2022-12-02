from django.urls import path, include
from rest_framework.routers import DefaultRouter

# # from applications.review.views import Review, DetailReview
#
from main.views import PostViewSet
from main import views

# router = DefaultRouter()
# router.register('posts', PostViewSet)

urlpatterns = [

    # path('categories/', views.CategoryListView(), name='categories-list'),
    # path('posts/', views.PostViewSet.as_view(), name='posts-list'),
    # path('posts/<int:pk>', views.Post)

    # path('auth/', include('rest_framework_social_oauth2.urls')),
    # path('review/', Review.as_view()),
    # path('reserv/', ReservationView.as_view()),
    # path('reserv-history/', ReservationHistory.as_view()),
    # # path('detail/<int:pk>/', DetailReview.as_view()),
    # path('favourite/', Favourite.as_view()),
    # path('', include(router.urls)),
    # path('favourite-history/', ),
]