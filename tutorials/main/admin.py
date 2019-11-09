from django.contrib import admin
from tinymce import widgets, TinyMCE
from django.db import models
from .models import Tutorial


class TutorialAdmin(admin.ModelAdmin):
    list_display = ['tutorial_title','tutorial_published']
    search_fields = ['tutorial_content','tutorial_content']

    class Meta:
        model=Tutorial

    formfield_overrides = {
        models.TextField:{'widget':TinyMCE()}
    }




admin.site.register(Tutorial,TutorialAdmin)