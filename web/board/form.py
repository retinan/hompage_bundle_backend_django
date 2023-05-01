from django.forms import *
from web.models import *


class BoardForm(ModelForm):
    upload = ImageField(label='첨부 이미지', required=False,
                             widget=FileInput(attrs={'class': 'form', 'multiple': True}))

    class Meta:
        model = Board
        fields = ('title', 'content',)


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        exclude = ('user', 'board',)
