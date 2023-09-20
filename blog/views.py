from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from django.core.paginator import Paginator

class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3

# def post_list(request):
#     post_list = Post.objects.filter(status=1).order_by('-created_on')
#     # Create a Paginator instance with a specified number of posts per page
#     paginator = Paginator(post_list, 3)
#     # Get the current page number from the request's GET parameters
#     page_number = request.GET.get('page')
#     # Get the Page object for the current page
#     page = paginator.get_page(page_number)
#     return render(request, 'index.html', {'page': page})

class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked=False
        if post.likes.filter(id=self.request.user.id).exists():
            liked=True

        return render(request, 'post_detail.html', {
            'post': post,
            'comments': comments,
            'liked': liked,
        })
