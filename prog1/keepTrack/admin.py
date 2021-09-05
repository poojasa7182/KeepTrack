from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Users)
admin.site.register(Project)
admin.site.register(List)
admin.site.register(Card)
admin.site.register(Comment_p)
admin.site.register(Comment_c)