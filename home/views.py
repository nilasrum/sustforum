from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import UserForms,LoginForm
from .models import Post,Comment,Reply,PostTag,Tag
from datetime import datetime
from django.core.urlresolvers import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404


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

class IndexView(generic.ListView):
    template_name = 'home/index.html'
    context_object_name = 'all_post'
    def get_queryset(self):
        return Post.objects.all()

class SinglePost(generic.DetailView):
    model = Post
    template_name = 'home/single_post.html'

# def single_post(request,post_id):
#     post = get_object_or_404(Post,pk=post_id)
#     context = {'post': post}
#     return render(request, 'home/single_post.html', context)

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

@method_decorator(login_required, name='dispatch')
class UpdatePost(UpdateView):
    model = Post
    fields = ['title','post']

@method_decorator(login_required, name='dispatch')
class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('home:index')