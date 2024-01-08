from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LikeQuestion)
admin.site.register(LikeAnswer)