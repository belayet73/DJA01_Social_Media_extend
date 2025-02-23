from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import profile, PostDetailView,PostUpdateView,PostDeleteView, PostCreateView, ProfileUpdateView, register, create_post, edit_post, delete_post

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('my_post/', views.my_post, name='my_post'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    
    path('core/new/', PostCreateView.as_view(), name='post-create'),
    path('core/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('core/<int:pk>/', PostDetailView.as_view(), name='post-detail'), 
    path('core/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    

    # Password reset views
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]

    