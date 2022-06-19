from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Pipeline, Category

# Create your views here.
class PipelineListView(ListView):
    model = Pipeline
    # template_name = 'client/index.html'

    def get_context_data(self, **kwargs):
        context = super(PipelineListView, self).get_context_data()
        # context['categories'] = Category.objects.all()
        # context['no_category_pipeline_count'] = Pipeline.objects.filter(category=None).count()
        return context