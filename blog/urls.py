from django.urls import path
from blog.views import (
    create_blog_view,
    post_list,
    post_detail,
    comment_added_view,
)
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from .feeds import LatestPostsFeed

sitemaps = {'posts': PostSitemap(), }

app_name = 'blog'

urlpatterns = [
    path('create', create_blog_view, name='create'),
    path('', post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('comment_added',comment_added_view,name='comment_added')
]


#     path('<int:post_id>/share/', views.post_share, name='post_share'),
#
#     path('search/', views.post_search, name='post_search'),

# ]
