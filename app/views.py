from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View, DetailView

from app.forms import CommentForm
from app.models import Profile, Post, Comment, Bookmark


class MainView(TemplateView):
    template_name = 'app/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['posts'] = Post.objects.all().order_by('-created_at')

        # Add a dictionary to check bookmarks
        if user.is_authenticated:
            bookmarks = {bookmark.post.id for bookmark in user.profile.bookmark_set.all()}
            context['bookmarks'] = bookmarks
        else:
            context['bookmarks'] = set()

        return context

class MyProfileView(TemplateView):
    template_name = 'app/my-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(user=self.request.user)
            my_posts = Post.objects.filter(profile=profile).order_by('-created_at')
            context['profile'] = profile
            context['posts'] = my_posts
        except Profile.DoesNotExist:
            return redirect('edit-my-profile')
        return context


class CreateNewPostView(CreateView):
    model = Post
    fields = ['description', 'photo']
    template_name = 'app/create-new-post.html'
    success_url = reverse_lazy('my-profile')

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class UpdateMyProfileView(UpdateView):
    model = Profile
    fields = ['photo', 'bio', 'age']
    template_name = 'app/edit-my-profile.html'
    success_url = reverse_lazy('my-profile')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'app/post_confirm_delete.html'
    success_url = reverse_lazy('my-profile')

    def get_object(self, queryset=None):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, id=post_id, profile__user=self.request.user)
        return post


def like_post(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponse(status=204)
    return HttpResponse(status=400)


class PostDetailView(TemplateView):
    template_name = 'app/comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post).order_by('-created_at')
        form = CommentForm()
        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)

        # Ensure the user has a profile
        if not hasattr(request.user, 'profile'):
            Profile.objects.create(user=request.user)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.profile = request.user.profile
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)

        return self.get(request, *args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'app/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(Profile, user__id=user_id)


@login_required
def toggle_bookmark(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    profile = request.user.profile
    bookmark, created = Bookmark.objects.get_or_create(profile=profile, post=post)

    if not created:
        bookmark.delete()

    return redirect('main')


class BookmarkListView(TemplateView):
    template_name = 'app/bookmarks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile
        bookmarks = Bookmark.objects.filter(profile=user_profile).select_related('post')
        posts = [bookmark.post for bookmark in bookmarks]
        context['posts'] = posts
        return context

