from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article, Category, Comment, ArticleRating
from .forms import CommentForm, RatingForm

class ArticleHomeView(ListView):
    model = Article
    template_name = 'articles/home.html'
    context_object_name = 'articles'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Featured articles for slider
        context['featured_articles'] = Article.objects.filter(
            is_featured=True, 
            status='published'
        )[:4]
        
        # Categories list
        context['categories'] = Category.objects.all()
        
        # Latest articles with pagination
        latest_articles = Article.objects.filter(
            status='published'
        ).order_by('-created_at')
        paginator = Paginator(latest_articles, 10)
        page = self.request.GET.get('page')
        context['latest_articles'] = paginator.get_page(page)
        
        # Most viewed articles
        context['most_viewed'] = Article.objects.filter(
            status='published'
        ).order_by('-view_count')[:5]
        
        # Most popular (by rating)
        context['most_popular'] = Article.objects.filter(
            status='published'
        ).annotate(
            avg_rating=Avg('ratings__score')
        ).order_by('-avg_rating')[:5]
        
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        
        # Increment view count
        article.view_count += 1
        article.save()
        
        # Comments
        context['comments'] = article.comments.filter(
            is_approved=True, 
            parent=None
        ).order_by('-created_at')
        context['comment_form'] = CommentForm()
        
        # Rating
        context['rating_form'] = RatingForm()
        if self.request.user.is_authenticated:
            context['user_rating'] = ArticleRating.objects.filter(
                article=article,
                user=self.request.user
            ).first()
        
        # Related articles (same category)
        context['related_articles'] = Article.objects.filter(
            category=article.category,
            status='published'
        ).exclude(id=article.id)[:3]
        
        return context

class CategoryArticlesView(ListView):
    model = Article
    template_name = 'articles/category_articles.html'
    context_object_name = 'articles'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        queryset = Article.objects.filter(
            category=self.category,
            status='published'
        )
        
        # Filtering
        filter_by = self.request.GET.get('filter')
        if filter_by == 'most_viewed':
            queryset = queryset.order_by('-view_count')
        elif filter_by == 'most_rated':
            queryset = queryset.annotate(
                avg_rating=Avg('ratings__score')
            ).order_by('-avg_rating')
        elif filter_by == 'latest':
            queryset = queryset.order_by('-created_at')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ArticleSearchView(ListView):
    model = Article
    template_name = 'articles/search_articles.html'
    context_object_name = 'articles'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Article.objects.filter(status='published')
        
        # Search query
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(summary__icontains=q)
            )
            
        # Advanced filters
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
            
        date_from = self.request.GET.get('date_from')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
            
        date_to = self.request.GET.get('date_to')
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
            
        min_rating = self.request.GET.get('min_rating')
        if min_rating:
            queryset = queryset.annotate(
                avg_rating=Avg('ratings__score')
            ).filter(avg_rating__gte=min_rating)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Add search parameters to context for form
        context['search_params'] = self.request.GET
        return context

@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            
            # Handle reply to comment
            parent_id = request.POST.get('parent_id')
            if parent_id:
                parent = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent
                
            comment.save()
            return redirect('article_detail', slug=article.slug)
    return redirect('article_detail', slug=article.slug)

@login_required
def rate_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = ArticleRating.objects.update_or_create(
                article=article,
                user=request.user,
                defaults={'score': form.cleaned_data['score']}
            )
    return redirect('article_detail', slug=article.slug)