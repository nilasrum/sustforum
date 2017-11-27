from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    #post list
    url(r'^$',views.IndexView.as_view(),name='index'),
    #register
    url(r'^register/$',views.RegistrationFormView.as_view(),name='register'),
    #login
    url(r'^login/$',views.login_form_view,name='login'),
    #logout
    url(r'^logout/$',views.logout_view,name='logout'),
    #single post details
    url(r'^(?P<pk>[0-9]+)/$',views.SinglePost.as_view(),name='single_post'),
    #add new post
    url(r'^post/newpost/$',views.AddPost.as_view(),name='new_post'),
    #update post
    url(r'^post/update/(?P<pk>[0-9]+)/$',views.UpdatePost.as_view(),name='update_post'),
    #delete post
    url(r'^post/delete/(?P<pk>[0-9]+)/$',views.DeletePost.as_view(),name='delete_post'),
]
