from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Like,  Profile
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import PostForm, RegistrationForm, ProfileForm,  AvatarUploadForm, CommentForm 
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import View
from django.http import request
from django.template.loader import render_to_string


def index(request):
    posts = Post.objects.all()
    context = {'posts': posts, 'title': 'Home'}
    return render(request, 'index.html', context)


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home.html', {'posts': posts})
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        files = request.FILES
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])
        if 'comment' in data:
                post_id = data.get('post_id')
                post = Post.objects.get(id=post_id)
                form = CommentForm(data)
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                context = {
                'comment_html': f'<div class="comment"><p>{comment.author}: {comment.content}</p></div>'
                    }
                return JsonResponse(context)
                
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

class AddCommentView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            context = {
                'comment_html': f'<div class="comment"><p>{comment.author}: {comment.content}</p></div>'
            }
            return JsonResponse(context)
        return JsonResponse({'error': 'Invalid form data.'}, status=400)

class LikePostView(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        existing_like = Like.objects.filter(user=user, post=post).first()
        if existing_like:
            existing_like.delete()
        else:
            like = Like(user=user, post=post)
            like.save()
        likes_count = post.likes.count()
        return JsonResponse({'likes_count': likes_count})


class LogoutPage(LogoutView):
    pass


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')


class PostView(PostForm):
    template_name = 'Post.html'

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post, parent_comment=None)
        return render(request, self.template_name, {'post': post, 'comments': comments})

    def post(self, request, *args, **kwargs):
        data = request.POST
        files = request.FILES
        user = self.request.user
        post = Post.objects.get(id=self.kwargs['pk'])
        if 'image' in files:
            image = files['image']
            post.image = image
            post.save()
            return redirect('post', pk=post.pk)
            

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

    


class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        avatar_form = AvatarUploadForm()
        context = {
            'user': user,
            'avatar_form': avatar_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            profile.avatar = form.cleaned_data['avatar']
            profile.save()
            return redirect('/profile')
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