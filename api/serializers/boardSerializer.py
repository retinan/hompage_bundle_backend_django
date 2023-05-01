from rest_framework import serializers
from web.models import Board, Comment


class CommentSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Comment
        fields = "__all__"
        ordering = ["-created_date"]


class BoardSerializers(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    comments = CommentSerializers(many=True, read_only=True)
    title = serializers.CharField(max_length=100, error_messages={
        'blank': '제목을 입력해주세요.',
        'max_length': '최대 100자까지 입력 가능 합니다.'
    })
    content = serializers.CharField(max_length=1000, error_messages={
        'required': 'please required',
        'blank': '내용을 입력해주세요.',
        'max_length': '최대 1000자까지 입력 가능 합니다.'
    })

    class Meta:
        model = Board
        fields = ['id', 'created_date', 'modified_date', 'title', 'content', 'image', 'user', 'comments']
        ordering = ["-created_date"]

