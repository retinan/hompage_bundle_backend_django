import os
import mimetypes
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import *
from .form import BoardForm, CommentForm
from web.models import *
from ..exceptions import FileUploadException


class BoardListView(ListView):
    model = Board
    template_name = 'board/list.html'
    context_object_name = 'boards'
    paginate_by = 10
    # paginate_orphans = 3  # 짜투리 처리
    ordering = "-created_date"  # 정렬 기준
    page_kwarg = "page"  # 페이징할 argument

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['test'] = 'test'
        return context


class BoardCreateView(CreateView):
    model = Board
    form_class = BoardForm
    template_name = 'board/create.html'
    success_url = reverse_lazy('board:list')

    def form_valid(self, form):
        board_form = form.save(commit=False)
        # user = self.request.user
        user = User.objects.get(id=1)  # 임시
        board_form.user = user
        if self.request.FILES['upload']:
            board_form.image = self.request.FILES['upload']
        board_form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context.update({"my_message": "Something went wrong"})
        return self.render_to_response(context)


class BoardDetailView(DetailView):
    model = Board
    template_name = 'board/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        board = get_object_or_404(Board, pk=pk)
        context['comments'] = Comment.objects.filter(board=board)
        return context


class BoardUpdateView(UpdateView):
    model = Board
    form_class = BoardForm
    template_name = 'board/update.html'

    def form_valid(self, form):
        board_form = form.save(commit=False)
        if self.request.FILES:
            board = Board.objects.get(id=self.kwargs['pk'])
            # 기존 이미지가 새 이미지로 교체되는 경우 기존 이미지 삭제
            if board.image:
                os.remove(os.path.join(settings.MEDIA_ROOT, board.image.path))
            board_form.image = self.request.FILES['upload']
        board_form.save()
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy('board:detail', kwargs={'pk': pk})


class BoardDeleteView(DeleteView):
    model = Board
    success_url = reverse_lazy('board:list')

    def get(self, request, **kwargs):
        return self.post(self, request, **kwargs)

    def form_valid(self, form):
        # 글삭제 시 해당 이미지도 삭제
        board = Board.objects.get(id=self.kwargs['pk'])
        if board.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, board.image.path))
        return super().form_valid(form)


@require_POST
def comment_create(request, pk):
    board = get_object_or_404(Board, pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.board = board
        comment.user = User.objects.get(id=2)
        comment.save()
    return redirect('board:detail', board.pk)


@require_POST
def comment_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()

    return redirect('board:detail', board_pk)
