from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from bs4 import BeautifulSoup
from urllib.request import urlopen
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Pipeline, Category, Tag, RequestHistory, Stage, Request
from . import enums
from .forms import CommentForm, StageForm, RequestForm, RequestHistoryForm

def index(request):
    pipelines = Pipeline.objects.all().order_by('-pk')
    stages = Stage.objects.all().order_by('-pk')
    requests = Request.objects.all().order_by('-pk')
    histories = RequestHistory.objects.all().order_by('-pk')

    return render(request, 'client/index.html', { 'pipelines': pipelines, 'stages': stages, 'requests': requests, 'histories': histories })

class HistoryList(ListView):
    model = RequestHistory
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(HistoryList, self).get_context_data()
        context['histories'] = RequestHistory.objects.all().order_by('-pk')
        return context

class HistoryDetail(DetailView):
    model = RequestHistory

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(StageDetail, self).get_context_data()
    #     request = Stage.objects.get(pk=self.kwargs['pk']);
    #     # context['request'] = request
    #     # context['histories'] = request.requests.all();
    #     return context

def request_detail(request, pk):
    detail = Request.objects.get(pk=pk)
    histories = RequestHistory.objects.filter(request=detail)

    return render(request, 'client/request_detail.html', {
                      'detail': detail,
                        'histories': histories,
                  })

class StageDetail(DetailView):
    model = Stage
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StageDetail, self).get_context_data()
        context['request_form'] = RequestForm
        stage = Stage.objects.get(pk=self.kwargs['pk']);
        context['requests'] = stage.requests.all();
        return context

# Create your views here.
class PipelineList(ListView):
    model = Pipeline
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context = super(PipelineList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['pipelines'] = Pipeline.objects.all().order_by('-pk')
        context['no_category_pipeline_count'] = Pipeline.objects.filter(category=None).count()
        return context

def requestMap(stage):
    # stage.requests = stage.requests.all()
    return stage

class PipelineDetail(DetailView):
    model = Pipeline

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PipelineDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_pipeline_without_category'] = Pipeline.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        stages = Stage.objects.filter(pipeline=self.kwargs['pk']);
        context['stages'] = map(requestMap, stages)
        context['stage_form'] = StageForm
        return context

class PipelineUpdate(LoginRequiredMixin, UpdateView ):
    model = Pipeline
    fields = ['title', 'description', 'hook_msg', 'head_image', 'attached_file', 'category', 'aggregated_status', 'pipe_line_status']

    template_name = 'client/pipeline_form_update.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PipelineUpdate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_pipeline_without_category'] = Pipeline.objects.filter(category=None).count()
        return context

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author :
            return super(PipelineUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

class PipelineCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Pipeline
    fields = ['title', 'description', 'hook_msg', 'head_image', 'attached_file', 'category', 'aggregated_status', 'pipe_line_status']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PipelineCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_pipeline_without_category'] = Pipeline.objects.filter(category=None).count()
        return context

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            return super(PipelineCreate, self).form_valid(form)
        else :
            return redirect('/')

def show_category_pipelines(request, slug):
    if slug=='no-category' :
        category = '미분류'
        pipeline_list = Pipeline.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        pipeline_list = Pipeline.objects.filter(category=category)

    context = {
        'categories' : Category.objects.all(),
        'count_pipeline_without_category' : Pipeline.objects.filter(category=None).count(),
        'category' : category,
        'pipelines' : pipeline_list
    }
    return render(request, 'client/pipeline_list.html', context)

def show_tag_pipelines(request, slug):
    tag = Tag.objects.get(slug=slug)
    pipelines = tag.pipeline_set.all()

    context = {
        'categories': Category.objects.all(),
        'count_pipeline_without_category': Pipeline.objects.filter(category=None).count(),
        'tag': tag,
        'pipelines': pipelines
    }
    return render(request, 'pipeline_list.html', context)


def addComment(request, pk):
    if request.user.is_authenticated:
        pipeline = get_object_or_404(Pipeline, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.pipeline = pipeline
            comment.save()
            return redirect(comment.get_absolute_url())
        else :
            return redirect(pipeline.get_absolute_url())
    else:
        raise PermissionDenied

def addStage(request, pk):
    if request.user.is_authenticated:
        pipeline = get_object_or_404(Pipeline, pk=pk)

        # 'title', 'description', 'pipeline'
        if request.method == "POST":
            stage_form = StageForm(request.POST)
            stage = stage_form.save(commit=False)
            # stage.title = 'new stage'
            stage.description = 'new stage description'
            stage.pipeline = pipeline

            stage.status = 'INITIATED'
            stage.pipe_line_status = 'INITIATED'
            stage.save()
            return redirect(pipeline.get_absolute_url())
        else :
            return redirect(pipeline.get_absolute_url())
    else:
        raise PermissionDenied

def addRequest(request, pk):
    if request.user.is_authenticated:
        stage = get_object_or_404(Stage, pk=pk)

        # 'title', 'description', 'pipeline'
        if request.method == "POST":
            request_form = RequestForm(request.POST)
            request = request_form.save(commit=False)
            request.description = 'new request'
            request.stage = stage
            request.save()
            stage.requests.add(request)
            stage.save()
            return redirect(stage.get_absolute_url())
        else :
            return redirect(stage.get_absolute_url())
    else:
        raise PermissionDenied

def execRequest(request, pk):
    if request.user.is_authenticated:
        detail = get_object_or_404(Request, pk=pk)

        if request.method == "POST":
            request_history_form = RequestHistoryForm(request.POST)
            request_history = request_history_form.save(commit=False)
            request_history.name = detail.name + '요청...'
            request_history.request = detail
            request_history.status = 'FAILED'
            request_history.save()

            soup = BeautifulSoup(urlopen(detail.url), 'html.parser', from_encoding="euc-kr")
            cur_price = soup.find("p", {"class":"no_today"})
            cur_rate = cur_price.find("span", {"class":"blind"})

            request_history.status = 'COMPLETED'
            request_history.result = cur_rate.text
            request_history.save()
            return redirect(detail.get_absolute_url())
        else :
            return redirect(detail.get_absolute_url())
    else:
        raise PermissionDenied

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        redirect('/')
    return render(request,'/')