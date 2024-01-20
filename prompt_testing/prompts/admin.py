from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Prompt)
admin.site.register(PromptGen)
admin.site.register(Evaluation)
admin.site.register(Rating)