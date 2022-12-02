# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
# from rest_framework.decorators import action
# from rest_framework.filters import SearchFilter
# from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
#
# from main.filter import ProductFilter
# from main.serializers import *
# # from applications.review.models import Like, Rating
# # from applications.review.serializers import RatingSerializer
#
#
# class LargeResultsSetPagination(PageNumberPagination):
#     """
#     Представление пагинации
#     """
#     page_size = 4
#     page_size_query_param = 'page_size'
#     max_page_size = 100
#
#
from main.models import Post, Category, PostImage
from main.serializers import PostSerializer, CategorySerializer, PostImageSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostImageView(ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class PostViewSet(ModelViewSet):
    """
    Представление отелей
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

#     pagination_class = LargeResultsSetPagination
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_class = ProductFilter
#     search_fields = ['title', 'description']

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




#
#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:
#             permissions = []
#         elif self.action == 'rating':
#             permissions = [IsAuthenticated]
#         else:
#             permissions = [IsAuthenticated]
#         return [permission() for permission in permissions]
#
#     @action(methods=['POST'], detail=True)
#     def recomendation(self, request, pk):
#         element_id = Element.objects.get(id=pk)
#         category_of_element = element_id.category
#         recomendation_element = Element.objects.filter(category=category_of_element)
#         serializer = ElementSerializer(recomendation_element, many=True)
#
#         return Response(serializer.data)
#
#     @action(methods=['POST'], detail=True)
#     def like(self, request, pk):
#         element = self.get_object()
#         like_obj, _ = Like.objects.get_or_create(element=element, user=request.user)
#         print(like_obj)
#         like_obj.like = not like_obj.like
#         like_obj.save()
#         status = 'liked'
#         if not like_obj.like:
#             status = 'unliked'
#         return Response({'status': status})
#
#     @action(methods=['POST'], detail=True)
#     def rating(self, request, pk):
#         serializer = RatingSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             obj = Rating.objects.get(element=self.get_object(), user=request.user)
#             obj.rating = request.data['rating']
#         except Rating.DoesNotExist:
#             obj = Rating(user=request.user, element=self.get_object(), rating=request.data['rating'])
#
#         obj.save()
#         return Response(request.data, status=status.HTTP_201_CREATED)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# class Favourite(ListCreateAPIView):
#     """
#     Представление избранных
#     """
#     queryset = FavouriteElement.objects.all()
#     serializer_class = FavouriteElementSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = super().get_queryset()
#         queryset = queryset.filter(user=user)
#         return queryset
#
#     def perform_create(self, serializer):
#         # print('\n\n', self.request.data, '\n\n')
#         serializer.save(user=self.request.user)
#
#
# class ReservationView(CreateAPIView):
#     """
#     Представление бронировании отелей
#     """
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#
#     def perform_create(self, serializer, ):
#         serializer.save(user=self.request.user)
#
#
# class ReservationHistory(ListAPIView):
#     """
#     Представление истории бронировании отелей
#     """
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#
#     def perform_create(self, serializer,):
#         serializer.save(user=self.request.user)
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = super().get_queryset()
#         queryset = queryset.filter(user=user)
#         return queryset
#
#
#
