from django.contrib import admin
from .models import  *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Tag)
admin.site.register(PostTag)
admin.site.register(PostVote)
admin.site.register(CommentVote)
admin.site.register(PostFollowed)
admin.site.register(UserInfo)
admin.site.register(Faq)
admin.site.register(
    Room,
    list_display=["id", "title", "staff_only"],
    list_display_links=["id", "title"],
)
