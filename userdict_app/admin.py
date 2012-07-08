from django.contrib import admin
from userdict_app import models

admin.site.register(models.AlphabetLetters)
admin.site.register(models.Hieroglyphs)
admin.site.register(models.Words)
