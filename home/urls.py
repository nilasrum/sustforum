from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    #post list
    url(r'^$',views.index_view,name='index'),
    #register
    url(r'^register/$',views.RegistrationFormView.as_view(),name='register'),
    #login
    url(r'^login/$',views.login_form_view,name='login'),
    #logout
    url(r'^logout/$',views.logout_view,name='logout'),
    #profile
    url(r'^user/(?P<user_id>[0-9]+)/profile/$',views.profile_view,name='profile'),
    #profile update
    url(r'^user/(?P<pk>[0-9]+)/profile/update/$',views.UpdateProfile.as_view(),name='profile_update'),
    #single post details
    url(r'^(?P<post_id>[0-9]+)/$',views.single_post,name='single_post'),
    #add new post
    url(r'^post/newpost/$',views.AddPost.as_view(),name='new_post'),
    #update post
    url(r'^post/update/(?P<pk>[0-9]+)/$',views.UpdatePost.as_view(),name='update_post'),
    #delete post
    url(r'^post/delete/(?P<pk>[0-9]+)/$',views.DeletePost.as_view(),name='delete_post'),
    #post comment
    url(r'^post/comment/(?P<post_id>[0-9]+)/$',views.post_comment,name='post_comment'),
    #commnet_delete
    url(r'^post/(?P<post_id>[0-9]+)/comment/(?P<cmnt_id>[0-9]+)/delete/$',views.comment_delete,name='comment_delete'),
    #comment_update
    url(r'^post/comment/(?P<cmnt_id>[0-9]+)/update/$',views.comment_update,name='comment_update'),
    #comment up/down vote
    url(r'^post/(?P<post_id>[0-9]+)/comment/(?P<cmnt_id>[0-9]+)/vote/(?P<vote_type>[0-1])$',views.comment_vote_handler,name='comment_vote'),
    #post follow
    url(r'^post/follow/(?P<post_id>[0-9]+)/$',views.post_follow,name='post_follow'),
    #post up down vote
    url(r'^post/(?P<post_id>[0-9]+)/vote/(?P<vote_type>[0-1])$',views.post_vote_handler,name='post_vote'),
]
