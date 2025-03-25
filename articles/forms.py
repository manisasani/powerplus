from django import forms
from .models import Article, Comment, ArticleRating

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'summary', 'featured_image', 'category', 'status', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter article title'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter a brief summary'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean_featured_image(self):
        image = self.cleaned_data.get('featured_image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
            
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
            import os
            ext = os.path.splitext(image.name)[1][1:].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError(
                    f"Unsupported file extension. Allowed extensions are: {', '.join(valid_extensions)}"
                )
        return image

    def clean_summary(self):
        summary = self.cleaned_data.get('summary')
        if len(summary) > 300:
            raise forms.ValidationError("Summary must be no more than 300 characters")
        return summary


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 5:
            raise forms.ValidationError("Comment must be at least 10 characters long")
        if len(text) > 1000:
            raise forms.ValidationError("Comment must be no more than 1000 characters")
        return text


class RatingForm(forms.ModelForm):
    class Meta:
        model = ArticleRating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'step': '1'
            })
        }

    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score < 1 or score > 5:
            raise forms.ValidationError("Rating must be between 1 and 5")
        return score