import json
import os

from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework import viewsets, pagination, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from web.board.form import CommentForm
from web.models import *
from api.serializers.boardSerializer import *


class BoardPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10


class BoardViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # queryset = Board.objects.prefetch_related('comments').all().order_by('-created_date')
    queryset = Board.objects.prefetch_related(
        Prefetch('comments', queryset=Comment.objects.order_by('-created_date'))).all().order_by('-created_date')
    serializer_class = BoardSerializers
    pagination_class = BoardPageNumberPagination

    @classmethod
    def as_view(cls, actions=None, **kwargs):
        cls.action = actions
        return super().as_view(actions=actions, **kwargs)

    def get_authenticators(self):
        authentication_classes = [JWTAuthentication]
        if self.action in ['list', 'retrieve']:
            authentication_classes = []
        return [auth() for auth in authentication_classes]

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # serializer.save(user=User.objects.get(id=1))
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):

        board = self.get_object()

        # 기존 이미지 삭제 처리를 위한 변수 초기화
        preimage_delete = False
        preimage_path = board.image.path if board.image else ''

        payloads = {
            'title': request.data.get('title', None),
            'content': request.data.get('content', None)
        }

        # 이미지 파일 업로드 처리
        image_file = request.FILES.get('image')
        if image_file:
            preimage_delete = bool(board.image)
            payloads['image'] = image_file
        else:
            # 기존 이미지 삭제 처리
            if request.data.get('isImageDelete') == 'true':
                preimage_delete = bool(board.image)
                payloads['image'] = None

        # 게시글 수정 정보 업데이트
        serializer = self.get_serializer(board, data=payloads, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 기존 이미지 삭제
        if preimage_delete:
            os.remove(os.path.join(settings.MEDIA_ROOT, preimage_path))

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        board = self.get_object()
        if request.user == board.user:
            self.perform_destroy(board)
        else:
            return Response({'error': '본인의 글만 삭제할 수 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if board.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, board.image.path))
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['board_pk'])

    def perform_create(self, serializer):
        serializer.save(user=User.objects.get(id=2), board_id=self.kwargs['board_pk'])


@csrf_exempt
@require_POST
def comment_create(request, pk):

    print(request.body)

    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        return JsonResponse({'error': 'Board does not exist'}, status=404)

    response_data = json.loads((request.body).decode())
    comment_form = CommentForm(response_data)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.board = board

        user, _ = JWTAuthentication().authenticate(request)
        print(user)
        if user:
            comment.user = user
        else:
            # user 객체가 없으면 인증 실패
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        comment.save()

        data = {
            'board_id': pk,
            'comment_id': comment.id,
            'comment_content': comment.content
        }
        return JsonResponse(data, status=200)
    else:
        return JsonResponse(comment_form.errors, status=400)

@csrf_exempt
@require_POST
def comment_delete(request, board_pk, comment_pk):
    print(request.body)
    try:
        status_code = 200
        comment = get_object_or_404(Comment, pk=comment_pk)
        user, _ = JWTAuthentication().authenticate(request)
        if user == comment.user:
            comment.delete()
        else:
            return JsonResponse({'error': '본인의 댓글만 삭제할 수 있습니다.'}, status=400)
        data = {
            'board_id': board_pk,
            'comment_id': comment_pk,
            'message': 'delete success'
        }
    except Exception as e:
        status_code = 404
        data = {
            'error': str(e)
        }

    return JsonResponse(data, status=status_code)
