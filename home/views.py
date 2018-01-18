from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import UserForms,LoginForm,CommentForm,UserInfoForm
from .models import Post,Comment,Reply,PostTag,Tag,PostVote,PostFollowed,CommentVote,Room,UserInfo,User
from datetime import datetime
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import itemgetter
import random


ara = ["#f9ecf9","#e6ffff","#f2ffcc","#e6f9ff","#e6ecff","#fff0b3","#f9e6ff"]

# login and logout and register

class RegistrationFormView(View):
    form_class = UserForms
    template_name = 'home/registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()


            #returns user objects if credentials is correct
            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    userinfo = UserInfo()
                    userinfo.user = user
                    userinfo.save()
                    login(request,user)
                    return redirect('home:index')

        return render(request,self.template_name,{'form':form})


def login_form_view(request):
    form = LoginForm(request.POST or None)
    template_name = 'home/login_form.html'

    if form.is_valid():

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # returns user objects if credentials is correct
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home:index')

    return render(request, template_name, {'form': form})

def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('home:index')
    raise Http404("user not loged in")

def index_view(request):
    template_name = 'home/index.html'
    all_post=[]
    all_posts = Post.objects.all().order_by('-id')
    for post in all_posts:
        temp=dict()
        temp['post']=post
        temp['color']=ara[random.randint(0, 6)]
        try:
            temp['uinfo']=UserInfo.objects.filter(user=post.author)[0]
            print temp['uinfo']
        except:
            pass
        all_post.append(temp)

    rooms = Room.objects.order_by("title")
    recent = Post.objects.all().order_by('-id')[:5]
    followed = []
    if request.user.is_authenticated():
        temp = PostFollowed.objects.filter(user=request.user).order_by('-id')[:5]
        for t in temp:
            followed.append(Post.objects.filter(pk=t.post_id)[0])

    query = request.GET.get("q")
    if query:
        all_post =all_post.filter(
            Q(title__icontains=query) |
            Q(post__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()

    paginator = Paginator(all_post, 10)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_posts = paginator.page(paginator.num_pages)

    context = {
        'all_post': paginated_posts,
        'recent': recent,
        'followed': followed,
        'room':rooms[0],
        'username':request.user.username
    }

    return render(request, template_name, context)

def single_post(request,post_id):
    post = get_object_or_404(Post,pk=post_id)
    edit = post.author==request.user
    delete = request.user.is_superuser
    recent = Post.objects.all().order_by('-id')[:5]
    comments = Comment.objects.filter(post=post)
    rooms = Room.objects.order_by("title")
    all_comments=[]
    for com in comments:
        wrap = dict()
        cuv = CommentVote.objects.filter(cmnt_id=com.pk, vote_type=1).count()
        cdv = CommentVote.objects.filter(cmnt_id=com.pk, vote_type=-1).count()
        com.vote = cuv - cdv
        reply = Reply.objects.filter(comment=com)
        wrap["comment"] = com
        try:
            wrap["propic"] = UserInfo.objects.get(user=com.author_id).propic.url
        except:
            pass
        wrap["reply"] = reply
        all_comments.append(wrap)

    follow = "unfollow"
    followed = []
    if request.user.is_authenticated():
        temp = PostFollowed.objects.filter(user=request.user).order_by('-id')[:5]
        for t in temp:
            followed.append(Post.objects.filter(pk=t.post_id)[0])
        f = PostFollowed.objects.filter(user=request.user,post_id=post_id).count()
        if f==0:
            follow = "follow"
    uv = PostVote.objects.filter(post_id=post_id,vote_type=1).count()
    dv = PostVote.objects.filter(post_id=post_id,vote_type=-1).count()
    vote = uv-dv
    temmp=0
    context = {
        'post': post,
        'edit':edit,
        'delete':delete,
        'vote':vote,
        'comments':all_comments,
        'follow':follow,
        'recent':recent,
        'followed':followed,
        'room':rooms[0],
        'username': request.user.username
    }
    return render(request, 'home/single_post.html', context)

@method_decorator(login_required, name='dispatch')
class AddPost(CreateView):
    model = Post
    fields = ['title','post']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.date = datetime.now()
        obj.save()
        return redirect(obj.get_absolute_url())

class UpdatePost(UpdateView):
    model = Post
    fields = ['title','post']

    def dispatch(self, request, *args, **kwargs):
        ru = get_object_or_404(Post,pk=kwargs['pk'])
        if ru.author==request.user:
            return super(UpdatePost, self).dispatch(
            request, *args, **kwargs)
        raise Http404("permission denied")


@method_decorator(staff_member_required, name='dispatch')
class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('home:index')

@login_required
def post_comment(request,post_id):
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.cleaned_data.get('comment')
        com = Comment()
        com.comment = comment
        com.post = Post.objects.get(pk=post_id)
        com.author_id = request.user
        com.date = datetime.now()
        com.save()

        return HttpResponse("<h1>"+str(com.get_last_id())+"</h1>")

    return render(request, 'home/comment_form.html', {'form': form,'post_id':post_id})


@login_required
def comment_delete(request,post_id,cmnt_id):
    post = get_object_or_404(Post,pk=post_id)
    cmnt = get_object_or_404(Comment,pk=cmnt_id)
    if cmnt.author_id==request.user or request.user.is_superuser or post.user==request.user:
        cmnt.delete()
        return redirect(cmnt.get_absolute_url())
    raise Http404('permission denied')

@login_required
def comment_update(request,cmnt_id):
    cmnt = get_object_or_404(Comment,pk=cmnt_id)
    form = CommentForm(request.POST or None)

    if cmnt.author_id==request.user:
        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            cmnt.comment = comment
            cmnt.date = datetime.now()
            cmnt.save()

            return redirect(cmnt.get_absolute_url())
        else:
            raise Http404('something went wrong')
    raise Http404('permission denied')


@login_required
def comment_vote_handler(request,post_id,cmnt_id,vote_type):
    vote_type=int(vote_type)
    obj = CommentVote()
    query = CommentVote.objects.filter(user=request.user,cmnt_id=cmnt_id)
    if len(query)==0:
        prev=0
        obj.user = request.user
        obj.post_id = post_id
        obj.cmnt_id = cmnt_id
        obj.vote_type = prev
    else:
        obj=query[0]
        prev=obj.vote_type
    #upvote
    if vote_type==1:
        if prev==1:
            raise Http404('already upvoted')
        else:
            obj.vote_type+=1
    elif vote_type==0:
        if prev==-1:
            raise Http404('already downvoted')
        else:
            obj.vote_type-=1

    obj.save()
    return redirect(obj.get_absolute_url())


@login_required
def post_vote_handler(request,post_id,vote_type):
    vote_type=int(vote_type)
    obj = PostVote()
    query = PostVote.objects.filter(user=request.user,post_id=post_id)
    if len(query)==0:
        prev=0
        obj.user = request.user
        obj.post_id = post_id
        obj.vote_type = prev
        print '****','not found'
    else:
        obj=query[0]
        prev=obj.vote_type
    #upvote
    if vote_type==1:
        if prev==1:
            raise Http404('already upvoted')
        else:
            obj.vote_type+=1
            print 'vote pos888888888888'
    elif vote_type==0:
        if prev==-1:
            raise Http404('already downvoted')
        else:
            obj.vote_type-=1

    obj.save()
    return redirect(obj.get_absolute_url())

@login_required
def post_follow(request,post_id):
    obj=PostFollowed()
    query=PostFollowed.objects.filter(user=request.user,post_id=post_id)
    if len(query)==0:
        obj.user = request.user
        obj.post_id = post_id
        obj.save()
    else:
        obj = query[0]
        obj.delete()
    return redirect(obj.get_absolute_url())

@login_required
def profile_view(request,user_id):
    puser = User.objects.get(pk=user_id)
    all_post = Post.objects.filter(author=puser)
    ttl = all_post.count()
    uv=dv=0
    mostv = []
    for post in all_post:
        wrap = dict()
        temp = PostVote.objects.filter(post_id=post.pk, vote_type=1).count()
        uv += temp
        dv += PostVote.objects.filter(post_id=post.pk, vote_type=-1).count()
        wrap['post']=post
        wrap['uv'] = temp
        mostv.append(wrap)
    mostv = sorted(mostv, key=itemgetter('uv'), reverse=True)[:5]
    uv /= ttl
    dv /= ttl
    uinfo = UserInfo.objects.get(user=puser)
    edit = request.user == puser
    pop = (uv/User.objects.all().count())*100
    context = {
        'uinfo':uinfo,
        'edit':edit,
        'ttl':ttl,
        'uv':uv,
        'dv':dv,
        'mostv':mostv,
        'pop':pop
    }
    return render(request, 'home/profile.html', context)


class UpdateProfile(UpdateView):
    model = UserInfo
    fields = ['firstname','lastname','profession','color','propic']

    def dispatch(self, request, *args, **kwargs):
        pu = get_object_or_404(User,pk=kwargs['pk'])
        if pu==request.user:
            return super(UpdateProfile, self).dispatch(
            request, *args, **kwargs)
        raise Http404("permission denied")

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        user = get_object_or_404(User,pk=pk)
        userinfo = get_object_or_404(UserInfo,user=user)
        return userinfo