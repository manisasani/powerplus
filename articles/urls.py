from django.urls import path
from .views import (
    ArticleHomeView, 
    ArticleDetailView, 
    CategoryArticlesView, 
    ArticleSearchView,
    add_comment,
    rate_article
)

app_name = "articles"

urlpatterns = [
    path('', ArticleHomeView.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryArticlesView.as_view(), name='category_detail'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('search/', ArticleSearchView.as_view(), name='search'),
    path('comment/<int:article_id>/', add_comment, name='add_comment'),
    path('comment/<int:article_id>/replay/<int:parent_id>/', add_comment, name='replay_comment'),
    path('rate/<int:article_id/', rate_article, name='rate_article'),
]
