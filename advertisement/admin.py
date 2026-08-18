from django.contrib import admin
from .models import Slideshow

@admin.register(Slideshow)
class SlideshowAdmin(admin.ModelAdmin):
    list_display = ('headline', 'button_text', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('headline', 'tagline')
    ordering = ('-created_at',)
    list_editable = ('button_text', 'is_active')
