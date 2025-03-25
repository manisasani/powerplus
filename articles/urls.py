from django.urls import path
from .views import (
    ArticleHomeView, 
    ArticleDetailView, 
    CategoryArticlesView, 
    ArticleSearchView,
    CategoryListView,
    add_comment,
    rate_article,
)

app_name = "articles"

urlpatterns = [
    path('', ArticleHomeView.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryArticlesView.as_view(), name='category_detail'),
    path('categories/', CategoryListView.as_view(), name='categories'), 
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('search/', ArticleSearchView.as_view(), name='search'),
    path('article/<slug:slug>/comment/', add_comment, name='add_comment'),
    path('article/<slug:slug>/rate/', rate_article, name='rate_article'),
]
