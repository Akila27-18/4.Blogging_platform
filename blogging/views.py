
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, SearchForm

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blogging/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        qs = Post.objects.select_related('author').prefetch_related('categories')
        query = self.request.GET.get("query") or ""
        category = self.request.GET.get("category") or ""
        if query:
            qs = qs.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query))
        if category:
            qs = qs.filter(categories__name=category)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_form"] = SearchForm(self.request.GET or None)
        ctx["categories"] = Category.objects.order_by('name')
        return ctx

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "blogging/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(approved=True)
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment submitted for moderation.")
            return redirect(self.object.get_absolute_url())
        messages.error(request, "There was a problem submitting your comment.")
        return self.get(request, *args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blogging/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blogging/post_form.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
    template_name = "blogging/post_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("post_list")
    else:
        form = UserCreationForm()
    return render(request, "blogging/register.html", {"form": form})

# Simple moderation views (staff only)
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

@staff_member_required
def moderation_queue(request):
    pending = Comment.objects.filter(approved=False).select_related('post','user')
    return render(request, "blogging/moderation_queue.html", {"pending": pending})

@staff_member_required
def approve_comment(request, pk):
    c = get_object_or_404(Comment, pk=pk)
    c.approved = True
    c.save()
    messages.success(request, "Comment approved.")
    return redirect("moderation_queue")
