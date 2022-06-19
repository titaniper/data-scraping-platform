from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Pipeline, Category, Tag, Request, RequestHistory, Stage

from .forms import CommentForm

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

class PipelineDetail(DetailView):
    model = Pipeline
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PipelineDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_pipeline_without_category'] = Pipeline.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
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
        'pipeline_list' : pipeline_list
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