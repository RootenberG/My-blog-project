from django import forms
from .models import Post, Comment


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']


class SearchForm(forms.Form):
    query = forms.CharField()


class UpdateBlogPostForm:
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']

        def save(self, commit=True):
            blog_post = self.instace
            blog_post.title = self.cleaned_data['title']
            blog_post.body = self.cleaned_data['body']
            if self.cleaned_data['image']:
                blog_post.image = self.cleaned_data['image ']
            if commit:
                blog_post.save()
            return blog_post 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
