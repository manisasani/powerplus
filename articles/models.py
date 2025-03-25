from django.db import models
from accounts.models import CustomUser
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.TextField(
        blank=True
    )
    image = models.ImageField(
        upload_to='categories/',
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    order = models.IntegerField(
        default=0,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:category_detail', kwargs={'slug': self.slug})

    
class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        allow_unicode=True,
        help_text="This field will be filled automatically"
    )
    content = RichTextUploadingField()
    summary = models.TextField(
        help_text="Brief summary of the article (max 300 characters)"
    )
    featured_image = models.ImageField(
        upload_to='articles/'
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
    )
    is_featured = models.BooleanField(
        default=False
    )
    view_count = models.PositiveIntegerField(
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'slug': self.slug})
    
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if not ratings:
            return 0.0
        return float(sum(rating.score for rating in ratings)) / len(ratings)
    

class ArticleRating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='article_ratings')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    class Meta:
        unique_together = ['article', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.article.title} - {self.score}"

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='article_comments')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    text = models.TextField()
    is_approved = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.article.title[:30]}"

    @property
    def is_parent(self):
        return self.parent is None

    @property
    def children(self):
        return self.replies.filter(is_approved=True)
