from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import Post, Comment, Like,  Profile
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import PostForm, RegistrationForm, ProfileForm
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib import messages
from .forms import AvatarUploadForm
from django.http import HttpResponseRedirect

def index(request):
    posts = Post.objects.all()
    context = {'posts': posts, 'title': 'Home'}
    return render(request, 'index.html', context)


class HomeView(ListView):
    template_name = 'home.html'
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['user'] = self.request.user
        return context


class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Неправильний логін або пароль')
        return super().form_invalid(form)




class LogoutPage(LogoutView):
    pass


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class PostView(PostForm):
    template_name = 'Post.html'

    def post(self, request, *args, **kwargs):
        data = request.POST
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])
        if 'text' in data.keys():
            comment = Comment(user=user, post=post, body=data['text'])
            comment.save()
            result = render_to_string('comment.html', {'user': user, 'comment': comment})
            return JsonResponse(result, safe=False)
        if 'like' in data.keys():
            like = Like.objects.filter(post=post)
            is_like = 0
            for i in like:
                if i.user == user:
                    i.delete()
                    break
            else:
                is_like = 1
                l = Like(post=post, user=user)
                l.save()
            return JsonResponse({'like_amount': len(Like.objects.filter(post=post)), 'isLike': is_like}, safe=False)
        if 'is_like' in data.keys():
            like = Like.objects.filter(post=post)
            for i in like:
                if i.user == user:
                    return JsonResponse({'like': 1}, safe=False)
            else:
                return JsonResponse({'like': 0}, safe=False)
        if 'id_comment' in data.keys():
            comment = Comment.objects.get(id=int(data['id_comment']))
            like = Like.objects.filter(comment=comment)
            for i in like:
                if i.user == user:
                    return JsonResponse({'like': 1, 'like_amount': len(Like.objects.filter(comment=comment))}, safe=False)
                else:
                    return JsonResponse({'like': 0, 'like_amount': len(Like.objects.filter(comment=comment))}, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        context['post'] = post
        context['user'] = self.request.user
        context['title'] = f'Post {post.id}'
        context['like_amount'] = len(Like.objects.filter(post=post))
        comments = Comment.objects.filter(post=post)
        c_likes = []
        for c in comments:
            c_likes.append([c, len(Like.objects.filter(comment=c))])
        context['comments'] = c_likes
        return context


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['posts'] = Post.objects.filter(author=user)
        context['title'] = 'Profile'
        context['avatar_form'] = AvatarUploadForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            profile = self.request.user
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return HttpResponseRedirect('/profile')
        else:
            return render(request, self.template_name, {'avatar_form': form})
    

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'Post.html', context)





def upload_avatar(request):
    if request.method == 'POST':
        avatar_url = 'шлях_до_завантаженої_картинки'


        return render(request, 'home.html', {'success': True, 'avatar_url': avatar_url})

    return render(request, 'upload_avatar.html')