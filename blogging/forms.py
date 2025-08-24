
from django import forms
from .models import Post, Comment, Category

class PostForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ["title", "content", "image", "categories"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Write a comment..."})
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False,
                            widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Search posts..."}))
