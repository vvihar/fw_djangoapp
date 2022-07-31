from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import TodoModel

# Create your views here.


class TodoList(ListView):
    template_name = 'todo/list.html'
    model = TodoModel


class TodoDetail(DetailView):
    template_name = 'todo/detail.html'
    model = TodoModel


class TodoCreate(CreateView):
    template_name = 'todo/create.html'
    model = TodoModel
    fields = ('title', 'memo', 'priority', 'duedate')
    # request -> responseの流れの逆 listはurls.pyで指定
    success_url = reverse_lazy('')


class TodoDelete(DeleteView):
    template_name = 'todo/delete.html'
    model = TodoModel
    success_url = reverse_lazy('') #成功時の遷移先

class TodoUpdate(UpdateView):
    template_name = 'todo/update.html'
    model = TodoModel
    fields = ('title', 'memo', 'priority', 'duedate')
    success_url = reverse_lazy('')
