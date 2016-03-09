from django.contrib import admin

# Register your models here.
from ScribaVitae.models import *

admin.site.register(Comment)
admin.site.register(LiteraryWork)
admin.site.register(Category)