from django.contrib import admin
from .models import  Post,Comment,Reply,Tag,PostTag

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Tag)
admin.site.register(PostTag)
