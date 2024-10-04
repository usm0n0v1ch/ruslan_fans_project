from django.urls import path

from app import views
from app.views import *

urlpatterns = [
    path('main/', MainView.as_view(), name='main'),
    path('my-profile/', MyProfileView.as_view(), name='my-profile'),
    path('create-new-post/', CreateNewPostView.as_view(), name='create-new-post'),
    path('edit-my-profile/<int:pk>/', UpdateMyProfileView.as_view(), name='edit-my-profile'),
    path('post-delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('profile/<int:user_id>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('toggle_bookmark/<int:post_id>/', toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks/', BookmarkListView.as_view(), name='bookmarks'),

]