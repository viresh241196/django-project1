from django import forms
from  .models import Post


class NewPostForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = Post
        fields = ['title','image','content']