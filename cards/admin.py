from django.contrib import admin

from .models import Project, CardType, Field, FieldData, Card

admin.site.register(Project)
admin.site.register(CardType)
admin.site.register(Field)
admin.site.register(Card)
admin.site.register(FieldData)
