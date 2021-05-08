from django.contrib import admin
from .models import Article

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Article, QuestionAdmin)