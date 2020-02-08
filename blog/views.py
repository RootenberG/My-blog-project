from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from blog.forms import CreateBlogPostForm
from account.models import Account
from django.db.models import Q
# from django.views.generic import ListView
# from django.contrib.postgres.search import TrigramSimilarity
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import EmailPostForm, CommentForm, SearchForm
from django.http import HttpResponse
# from django.core.mail import send_mail
from taggit.models import Tag
# from django.db.models import Count
from django.views.generic import TemplateView, ListView


def create_blog_view(request):
    contex = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()
    return render(request, 'blog/createblog.html', contex)


class post_search(ListView):
    model = Post
    template_name = 'blog/post/search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
        return object_list


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if request.GET:
        query = request.GET['q']
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # По 3 статьи на каждой странице.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)
    latest_posts = Post.published.all()[0:3]

    return render(request, 'blog/post/list.html',
                  {
                      'page': page,
                      'posts': posts,
                      'tag': tag,
                      'latest_posts': latest_posts,


                  })


def comment_added_view(request):
    return render(request, 'blog/post/comment_added.html', {})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year,
                             publish__month=month, publish__day=day)
    # Список активных комментариев для этой статьи.
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Пользователь отправил комментарий.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье.
            new_comment.post = post
            # Сохраняем комментарий в базе данных.
            new_comment.save()
            return redirect('blog:comment_added')
    else:
        comment_form = CommentForm()
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids)\
    #     .exclude(id=post.id)
    # similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
    #     .order_by('-same_tags', '-publish')[:4]
    similar = post.tags.similar_objects()
    return render(request,
                  'blog/post/detail.html', {
                      'post': post,
                      'comments': comments,
                      'new_comment': new_comment,
                      'comment_form': comment_form,
                      'similar_posts': similar,
                      'similar': similar
                  })
