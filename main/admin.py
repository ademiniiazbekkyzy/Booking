from django.contrib import admin

from main.models import *


admin.site.register(Comment)
admin.site.register(Booking)


class ImageInAdmin(admin.TabularInline):
    model = ElementImage
    fields = ('image', )
    max_num = 5


@admin.register(Element)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdmin
    ]
