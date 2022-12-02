import time

# from django.contrib.auth import get_user_model
from rest_framework import serializers
#
# from account.send_mail import mail_message
from .models import *
#
# from booking_api.tasks import send_mail_message
#
# token = '5350539323:AAEDs7_ttU8d84egZTdqsG977AKbXRd36GA'
# chat_id = '-566077291'
# text = 'admindnq'
#
#
# User = get_user_model()


class PostImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор фото
    """
    class Meta:
        model = PostImage
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории
    """
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор отелей
    """
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S')
    user = serializers.ReadOnlyField(source='user.email')
    image = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'user', 'category', 'image', 'created_at')
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         images_data = request.FILES
#         element = Element.objects.create(**validated_data)
#         for image in images_data.getlist('images'):
#             ElementImage.objects.create(element=element, image=image)
#         return element
#

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.images.all(), many=True, context=self.context).data
        # representation['like'] = instance.like.filter(like=True).count()
        # representation['reviews'] = instance.comment.count()

#         rating_result = 0
#         for i in instance.rating.all():
#             rating_result += int(i.rating)
#
#         if instance.rating.all().count() == 0:
#             representation['rating'] = rating_result
#
#         else:
#             representation[' rating'] = rating_result / instance.rating.all().count
#
        return representation
#
#
# class FavouriteElementSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор избранных
#     """
#
#     user = serializers.ReadOnlyField(source='user.email')
#
#     class Meta:
#         model = FavouriteElement
#         fields = '__all__'
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         user = request.user
#         product = validated_data.get('product')
#
#         if FavouriteElement.objects.filter(user=user, product=product):
#             return FavouriteElement.objects.get(user=user, product=product)
#         else:
#             return FavouriteElement.objects.create(user=user, product=product)
#
#
# class ReservationSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор бронировании отелей
#     """
#     user = serializers.ReadOnlyField(source='user.email')
#
#     class Meta:
#         model = Reservation
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         print('-----------------------')
#         print(instance)
#         representation['element'] = ElementSerializer(instance.element).data
#         return representation
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         print(request.data.get('element'))
#         a = request.data.get('element')
#         # TODO find
#         # b = Element.objects.get(a)
#         # print(b)
#
#
