from django.contrib import admin

from .models import Choice, MultipleChoiceQuestion, TrueFalseQuestion

admin.site.register(MultipleChoiceQuestion)
admin.site.register(TrueFalseQuestion)
admin.site.register(Choice)