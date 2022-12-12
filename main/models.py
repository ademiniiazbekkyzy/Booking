from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.generics import ListAPIView


User = get_user_model()


class Element(models.Model):
    """
    Моделька отелей
    """

    user = models.ForeignKey(User, related_name='elements', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    # category = models.ForeignKey(Category, related_name='elements', on_delete=models.CASCADE)
    # category = models.ForeignKey('Category', on_delete=models.CASCADE)
    # element_slug = models.SlugField(unique=True, null=True)
    is_booked = models.BooleanField(default=False)
    # cover_image = models.ImageField(upload_to=room_images_upload_path)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'


class ElementImage(models.Model):
    """
    Моделька Фото
    """
    image = models.ImageField(upload_to='images')
    element = models.ForeignKey(Element, related_name='image', on_delete=models.CASCADE)


# class Comment(models.Model):#     user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
#     element = models.ForeignKey(Element, related_name='comments', on_delete=models.CASCADE)
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"{self.user}->{self.element}->{self.created_at}-{self.body[0:10]}"


class Comment(models.Model):
    """
    Модель Отзывов
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    element = models.ForeignKey(Element, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.comment}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


# class CheckIn(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     element = models.ForeignKey(Element, on_delete=models.CASCADE, default='')
#     phone = models.CharField(max_length=14, null=True)
#     email = models.EmailField(null=True)
#
#     def __str__(self):
#         return self.element.element_slug
#
#
# class CheckOut(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     check_out_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user


class Booking(models.Model):
    TIMESLOT_LIST = (
        (0, '09:00 - 10:00'),
        (1, '10:00 - 11:00'),
        (2, '11:00 - 12:00'),
        (3, '12:00 - 13:00'),
        (4, '14:00 - 15:00'),
        (5, '15:00 - 16:00'),
        (6, '16:00 - 17:00'),
        (7, '17:00 - 18:00'),
    )

    element = models.ForeignKey(Element, related_name='booking', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='booking', on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    time_slot = models.IntegerField(choices=TIMESLOT_LIST,)
    date = models.DateField(help_text="YYYY-MM-DD")
    phone = models.CharField(max_length=30, default='-')

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.time_slot][1]


# class Comment(models.Model):
#     user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
#     element = models.ForeignKey(Element, related_name='comments', on_delete=models.CASCADE)
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Comment{self.user.username} -> {self.element.first_name} [{self.created_at}]"



