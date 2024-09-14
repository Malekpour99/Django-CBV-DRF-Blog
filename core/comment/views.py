from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Post
from comment.models import Comment


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    let authenticated user submit a comment for a blog post
    """

    template_name = "blog/post.html"
    model = Comment
    fields = ["subject", "message"]

    def form_valid(self, form):
        form.instance.commenter = self.request.user.profile
        form.instance.post = Post.objects.get(slug=self.kwargs["slug"])

        messages.add_message(
            self.request,
            messages.SUCCESS,
            "Comment submitted successfully! It will be published after approval.",
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("blog:post-detail", kwargs={"slug": self.kwargs["slug"]})
