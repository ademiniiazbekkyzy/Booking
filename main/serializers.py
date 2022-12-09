from datetime import datetime
import time
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from account.send_mail import mail_message
from main.models import Element, ElementImage, FavouriteElement, Reservation, CheckIn, Comment
import requests
# from main.sendmessage import sendTelegram
# from telebot.models import TeleSettings
from booking_api.tasks import send_mail_message

# token = '5350539323:AAEDs7_ttU8d84egZTdqsG977AKbXRd36GA'
# chat_id = '-566077291'
# text = 'admindnq'


User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор фотографий
    """
    class Meta:
        model = ElementImage
        fields = '__all__'


# class CategorySerializer(serializers.ModelSerializer):
#     """
#     Сериализатор категорий
#     """
#     class Meta:
#         model = Category
#         fields = '__all__'


class ElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор площадок
    """
    # user = serializers.ReadOnlyField(source='user.email')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Element
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        element = Element.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            ElementImage.objects.create(element=element, image=image)
        return element

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
        # representation['like'] = instance.like.filter(like=True).count()
        # representation['reviews'] = instance.comment.count()

        # rating_result = 0
        # for i in instance.rating.all():
        #     rating_result += int(i.rating)
        #
        # if instance.rating.all().count() == 0:
        #     representation['rating'] = rating_result
        #
        # else:
        #     representation[' rating'] = rating_result / instance.rating.all().count
        #
        # return representation


class FavouriteElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор избранных
    """

    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = FavouriteElement
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product = validated_data.get('product')

        if FavouriteElement.objects.filter(user=user, product=product):
            return FavouriteElement.objects.get(user=user, product=product)
        else:
            return FavouriteElement.objects.create(user=user, product=product)


class ReservationSerializer(serializers.ModelSerializer):
    """
    Сериализатор бронирования площадок
    """
    # user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Reservation
        fields = '__all__'


class CheckinSerializer(serializers.ModelSerializer):
    element_id = serializers.IntegerField(source='element.pk', default=datetime.now)
    element_slug = serializers.SlugField(source='element.element_slug', default=datetime.now)
    user_id = serializers.IntegerField(source='user.pk')
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = CheckIn
        fields = ('phone_number', 'email', 'user_id', 'user_name', 'element_id', 'element_slug',)


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов
    """
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Comment
        fields = '__all__'


class RetriveReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отзыва
    """
    class Meta:
        model = Element
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['review'] = ReviewSerializer(instance.comment.all(), many=True).data
        return representation

# TODO dqw
