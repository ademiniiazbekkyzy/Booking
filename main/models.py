# from datetime import timezone
from datetime import datetime
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
# from django.utils.timezone.now import timezone

User = get_user_model()


# class Category(models.Model):
#     """
#     Моделька категории
#     """
#     title = models.CharField(max_length=100)
#     slug = models.SlugField()
#     parent = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category', blank=True, null=True)
#
#     def __str__(self):
#         if not self.parent:
#             return f'{self.id}'
#         else:
#             return f'{self.parent} --> {self.slug}'
#
#     def save(self, *args, **kwargs):
#         self.slug = self.title.lower()
#         super(Category, self).save(*args, **kwargs)
#
#     class Meta:
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categories'


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
    # element_slug = models.SlugField(default='')
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


class FavouriteElement(models.Model):
    """
    Моделька избранных отелей
    """
    user = models.ForeignKey(User, related_name='favourite', on_delete=models.CASCADE)
    element = models.ForeignKey(Element, related_name='favourite', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Reservation(models.Model):
    """
    Моделька бронировании отели
    """

    user = models.ForeignKey(User, related_name='reservation', on_delete=models.CASCADE)
    element = models.ForeignKey(Element, related_name='reservation', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    checking_date = models.DateTimeField(blank=True, null=True, default=datetime.now) #
    checkout_date = models.DateTimeField(null=True, blank=True, default=datetime.now) #
    phone = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    # confirm_reservation = models.CharField(max_length=8, blank=True)

    def __str__(self):
        return f'{self.element.title}'


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, default='')
    phone_number = models.CharField(max_length=14, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.element.element_slug


class CheckOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_out_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user



class Comment(models.Model):
    """
    Модель Отзывов
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    element = models.ForeignKey(Element,on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.comment}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

