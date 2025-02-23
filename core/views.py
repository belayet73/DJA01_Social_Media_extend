from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.views.generic import DetailView,  UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy


from . models import Profile, Post, Comment, Like
from . forms import RegistrationForm, ProfileUpdateForm, PostForm, CommentForm

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    search_query = request.GET.get('q', None)
    if search_query:
        posts = posts.filter( 
        Q(title__icontains=search_query)|  
        Q(text__icontains=search_query)     
    ) 
    # Filter by media type
    media_type = request.GET.get('media')
    if media_type == "text":
        posts = posts.filter(image__isnull=True)
    elif media_type == "image":
        posts = posts.filter(image__isnull=False)

    
    # ✅ Filter by Author (Fix this part)
    author_username = request.GET.get('author')
    if author_username:
        try:
            author = User.objects.get(username=author_username)
            posts = posts.filter(author=author)
        except User.DoesNotExist:
            posts = Post.objects.none()  # Return no posts if user does not exist

    # Filter by date
    date_sort = request.GET.get('date')
    if date_sort == "latest":
        posts = posts.order_by('-created_at')
    elif date_sort == "oldest":
        posts = posts.order_by('created_at')

   # context = {'posts': posts}
   # return render(request, 'posts/post_list.html', context)
    return render(request, 'home.html', {'posts': posts})

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'
    context_object_name = 'post'  # Default is 'object'


# ✅ Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign current user as the post owner
        return super().form_valid(form)

# ✅ Edit an existing post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only post owner can edit


# ✅ DELETE: Allow users to delete their own posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Only post owner can delete


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')  # Redirect to profile after updating

    def get_object(self):
        return self.request.user.profile  # ✅ Fetch the correct profile instance

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(author=request.user)
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_post')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'form': form})



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #form.save()
            user = form.save()
            messages.success(request, 'Account created successfully!')
            #return redirect('login')
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('my_post')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('my_post')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, 'You do not have permission to update this post.')
        return redirect('my_post', id=post.id)
        #return redirect('home')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'create_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    #post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('post_details', id=post.id)
    post.delete()
    messages.success(request, 'Post deleted successfully.')
    return redirect('my_post')


@login_required(login_url='/login/')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
    return redirect('home')


@login_required(login_url='/login/')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    
    return render(request, 'add_comment.html', {'form': form})

def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    #categories = Category.objects.all()
    #tags = Tag.objects.all()
    #return render(request, 'post_details.html', {'post': post,  'categories': categories, 'tags': tags})
    return render(request, 'post_details.html', {'post': post})

@login_required
def my_post(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(author=request.user)
    search_query = request.GET.get('q', None)
    if search_query:
        posts = posts.filter( 
        Q(title__icontains=search_query)|  
        Q(text__icontains=search_query)     
    ) 
    return render(request, 'my_post.html', {'profile': profile, 'posts': posts})

    

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('my_post')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def logout_view(request):
    messages.info(request, "You have logged out.")
    return redirect('home')

