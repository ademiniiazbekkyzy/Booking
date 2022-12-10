from datetime import datetime
import time
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from account.send_mail import mail_message
from main.models import Element, ElementImage, Reservation, CheckIn, Comment
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


class ReservationSerializer(serializers.ModelSerializer):
    """
    Сериализатор бронирования площадок
    """
    # user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Reservation
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'user', 'element')


class BookingSerializer(serializers.ModelSerializer):
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
        fields = ('phone', 'email', 'user_id', 'user_name', 'element_id', 'element_slug',)


# class EntrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Entry
#         exclude = ['user']
#
#     def create(self, validated_data):
#         validated_data['user'] = self.context.get('request').user
#         return super().create(validated_data)
#
#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         rep["user"] = instance.user.email
#         return rep





