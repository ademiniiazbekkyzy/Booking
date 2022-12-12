# from django.shortcuts import
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import status, permissions, generics, mixins
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .tasks import entry_created
from main.permissions import IsAdminOrReadOnly, IsAuthor
from main.serializers import *


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
    search_fields = ['title', 'description']


class ElementAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    # permission_classes = [IsAdminOrReadOnly]


class ElementDestroy(generics.RetrieveDestroyAPIView):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    # permission_classes = [IsAdminOrReadOnly]



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


# class CheckoutView(APIView):
#     def post(self, request):
#         element = get_object_or_404(Element, pk=request.data['pk'])
#         checked_in_element = CheckIn.objects.get(element__pk=request.data['pk'])
#         print(checked_in_element)
#         element.is_booked = False
#         element.save()
#         checked_in_element.delete()
#         return Response({"Checkout Successful"}, status=status.HTTP_200_OK)
#
#
# class CheckedInView(ListAPIView):
#     permission_classes = (IsAdminUser, )
#     serializer_class = CheckinSerializer
#     queryset = CheckIn.objects.order_by('-id')


# class CommentListCreateView(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class EntryViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor]

    def create(self, request, *args, **kwargs):
        r_data = request.data
        date = r_data.get("date")
        time_slot = r_data.get("time_slot")
        element = r_data.get("element")
        entries = Booking.objects.filter(element=element)
        if entries:
            for e in entries:
                if str(e.date) == str(date) and str(e.time_slot) == str(time_slot):
                    return Response(
                        "This time slot is already booked for this zone. Please choose another time or day")
        super().create(request, *args, **kwargs)
        entry = Booking.objects.get(date=date, time_slot=time_slot, element=element)
        entry_created.delay(entry.id)
        return Response("Appointment created")

    def update(self, request, *args, **kwargs):
        r_data = request.data
        date = r_data.get("date")
        time_slot = r_data.get("time_slot")
        entries = Booking.objects.filter(element=r_data["element"])
        if entries:
            for e in entries:
                if str(e.date) == str(date) and str(e.time_slot) == str(time_slot):
                    return Response(
                        "This time slot is already booked for this facility. Please choose another time or day")
        return super().update(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ReservationHistory(ListAPIView):
    """
    Представление истории бронировании объектов
    """
    queryset = Booking.objects.all()
    serializer_class = EntrySerializer

    def perform_create(self, serializer,):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset

# class BookingCreateApiView(CreateAPIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = BookingSerializer
#     queryset = Reservation.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         response = {}
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         response['data'] = serializer.data
#         response['response'] = "Room is successfully booked"
#         return Response(response, status=status.HTTP_201_CREATED, headers=headers)
#
#     def post(self, request, *args, **kwargs):
#         element = get_object_or_404(Element, pk=request.data.get('element'))
#         print(element, '------')
#         if element.is_booked:
#             return Response({"response": "Room is already booked"}, status=status.HTTP_200_OK)
#         element.is_booked = True
#         element.save()
#         checked_in_element = CheckIn.objects.create(
#             user=request.user,
#             element=element,
#             phone=request.data.get('phone'),
#             email=request.data.get('email')
#         )
#         checked_in_element.save()
#         return self.create(request, *args, **kwargs)
#
#
# class CheckoutView(APIView):
#     def post(self, request):
#         element = get_object_or_404(Element, pk=request.data['pk'])
#         checked_in_element = CheckIn.objects.get(element__pk=request.data['pk'])
#         print(checked_in_element)
#         element.is_booked = False
#         element.save()
#         checked_in_element.delete()
#         return Response({"Checkout Successful"}, status=status.HTTP_200_OK)
#
#
# class CheckedInView(ListAPIView):
#     permission_classes = (IsAdminUser, )
#     serializer_class = CheckinSerializer
#     queryset = CheckIn.objects.order_by('-id')


# class CommentViewSet(mixins.CreateModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.DestroyModelMixin,
#                      GenericViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthor, IsAuthenticated]
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["request"] = self.request
#         return context


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
