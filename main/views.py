from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from rest_framework import status, permissions, generics
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# from main.filter import ProductFilter
from account.views import CustomView
from main.models import *
# from main.sendmessage import sendTelegram
from main.permissions import IsAdminOrReadOnly
from main.serializers import *
# from applications.review.models import Like, Rating
# from applications.review.serializers import RatingSerializer
# from parser import main

# from main.models import HotelsIk


class LargeResultsSetPagination(PageNumberPagination):
    """
    Представление пагинации
    """
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100


class ElementAPIList(generics.ListCreateAPIView):
    """
    Представление отелей
    """
    queryset = Element.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ElementSerializer

    # pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_class = ProductFilter
    search_fields = ['title', 'description']


    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         permissions = []
    #     elif self.action == 'rating':
    #         permissions = [IsAuthenticated]
    #     else:
    #         permissions = [IsAuthenticated]
    #     return [permission() for permission in permissions]



    # @action(methods=['POST'], detail=True)
    # def recomendation(self, request, pk):
    #     element_id = Element.objects.get(id=pk)
    #     category_of_element = element_id.category
    #     recomendation_element = Element.objects.filter(category=category_of_element)
    #     serializer = ElementSerializer(recomendation_element, many=True)
    #
    #     return Response(serializer.data)

    # @action(methods=['POST'], detail=True)
    # def like(self, request, pk):
    #     element = self.get_object()
    #     like_obj, _ = Like.objects.get_or_create(element=element, user=request.user)
    #     print(like_obj)
    #     like_obj.like = not like_obj.like
    #     like_obj.save()
    #     status = 'liked'
    #     if not like_obj.like:
    #         status = 'unliked'
    #     return Response({'status': status})

    # @action(methods=['POST'], detail=True)
    # def rating(self, request, pk):
    #     serializer = RatingSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         obj = Rating.objects.get(element=self.get_object(), user=request.user)
    #         obj.rating = request.data['rating']
    #     except Rating.DoesNotExist:
    #         obj = Rating(user=request.user, element=self.get_object(), rating=request.data['rating'])
    #
    #     obj.save()
    #     return Response(request.data, status=status.HTTP_201_CREATED)
    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ElementAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    # permission_classes = [IsAdminOrReadOnly]


class ElementDestroy(generics.RetrieveDestroyAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    # permission_classes = [IsAdminOrReadOnly]


class Favourite(ListCreateAPIView):
    """
    Представление избранных
    """
    queryset = FavouriteElement.objects.all()
    serializer_class = FavouriteElementSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        # print('\n\n', self.request.data, '\n\n')
        serializer.save(user=self.request.user)


class ReservationView(CreateAPIView):
    """
    Представление бронировании отелей
    """
    permission_classes = (IsAuthenticated,)
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer, ):
        serializer.save(user=self.request.user)


class ReservationHistory(ListAPIView):
    """
    Представление истории бронировании отелей
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer,):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset


class CheckoutView(APIView):
    def post(self, request):
        element = get_object_or_404(Element, pk=request.data['pk'])
        checked_in_element = CheckIn.objects.get(element__pk=request.data['pk'])
        print(checked_in_element)
        element.is_booked = False
        element.save()
        checked_in_element.delete()
        return Response({"Checkout Successful"}, status=status.HTTP_200_OK)


class CheckedInView(ListAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = CheckinSerializer
    queryset = CheckIn.objects.order_by('-id')



class Review(CreateAPIView):
    """
    Представление отзывов
    """
    queryset = Comment.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailReview(RetrieveAPIView):
    """
    Представление для детального отзыва с отзывами
    """
    serializer_class = RetriveReviewSerializer
    queryset = Element.objects.all()




