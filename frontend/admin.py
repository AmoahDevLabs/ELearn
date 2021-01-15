from django.contrib import admin
from .models import Page, FrontImage


class ImageInline(admin.TabularInline):
    model = FrontImage


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [ImageInline]

