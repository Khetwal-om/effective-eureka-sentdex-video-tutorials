from django.contrib import admin
from tinymce import widgets, TinyMCE
from django.db import models
from .models import Tutorial,TutorialCategory,TutorialSeries

from .models import Moments



class TutorialAdmin(admin.ModelAdmin):
    list_display = ['tutorial_title','tutorial_published','tutorial_slug','tutorial_series']
    search_fields = ['tutorial_content','tutorial_content']

    fieldsets = [
        ('title',{'fields':['tutorial_title','tutorial_published']}),
        ('url',{'fields':['tutorial_slug']}),
        ('Series',{'fields':['tutorial_series']}),
        ('Content',{'fields':['tutorial_content']})
    ]

    class Meta:
        model=Tutorial

    formfield_overrides = {
        models.TextField:{'widget':TinyMCE()}
    }



admin.site.register(TutorialCategory)
admin.site.register(TutorialSeries)
admin.site.register(Tutorial,TutorialAdmin)

admin.site.register(Moments)


