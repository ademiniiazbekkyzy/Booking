from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models

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
    element_slug = models.SlugField(unique=True, null=True)
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


class Reservation(models.Model):
    """
    Моделька бронировании отели
    """

    user = models.ForeignKey(User, related_name='reservation', on_delete=models.CASCADE)
    element = models.ForeignKey(Element, related_name='reservation', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    checking_date = models.DateTimeField(default=datetime.now) #
    checkout_date = models.DateTimeField(default=datetime.now) #
    phone = models.CharField(max_length=30)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.element.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    element = models.ForeignKey(Element, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}->{self.element}->{self.created_at}-{self.body[0:10]}"


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, default='')
    phone = models.CharField(max_length=14, null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.element.element_slug


class CheckOut(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_out_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


# class Entry(models.Model):
#     TIMESLOT_LIST = (
#         (0, '09:00 - 10:00'),
#         (1, '10:00 - 11:00'),
#         (2, '11:00 - 12:00'),
#         (3, '12:00 - 13:00'),
#         (4, '14:00 - 15:00'),
#         (5, '15:00 - 16:00'),
#         (6, '16:00 - 17:00'),
#         (7, '17:00 - 18:00'),
#     )
#
#     element = models.ForeignKey(Element, related_name='entrys', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='entrys', on_delete=models.CASCADE)
#     # service_listing = models.ForeignKey(ServiceListing, related_name='entrys', on_delete=models.CASCADE)
#     entrys_time = models.DateTimeField(auto_now_add=True)
#     # time_slot = models.IntegerField(many=True) # choices=TIMESLOT_LIST,
#     date = models.DateField(help_text="YYYY-MM-DD", many=True)
#
#     @property
#     def time(self):
#         return self.TIMESLOT_LIST[self.time_slot][1]


