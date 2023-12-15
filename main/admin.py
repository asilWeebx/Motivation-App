from django.contrib import admin
from .models import User, Category, Status, Authors, StatusUser

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Authors)
admin.site.register(StatusUser)