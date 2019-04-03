from django.views.generic import ListView, CreateView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
import csv
from django.contrib import messages
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from . import models
from .classifier import classify_defect
from datetime import datetime
import io
from django.shortcuts import render
from .tables import ArticleTable
from django.db.models import Q
from django_tables2.config import RequestConfig
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import ArticleFilter
from django.db.models import Count
from django.http import JsonResponse
import json



class FilteredArticleListView(SingleTableMixin, FilterView):
    table_class = ArticleTable
    model = models.Article
    template_name = 'table.html'

    filterset_class = ArticleFilter

'''
def article_table(request):

    article = models.Article.objects.all()

    search_term = ''

    if 'search' in request.GET:
        search_term = request.GET['search']
        article = article.filter(Q(body__icontains=search_term)|Q(source__icontains =search_term)|Q(id__icontains=search_term)|Q(classification__icontains=search_term))


    table = ArticleTable(article.order_by('-id'))

    RequestConfig(request).configure(table)
    context = {'search_term':search_term, 'article_table_instance': table}
    return render(request, 'table.html', context)
'''

class ArticleCreateView(CreateView):
    model = models.Article
    template_name = 'article_new.html'
    fields = ['body']


class FileError(TemplateView):
    model = models.Article
    template_name = 'error.html'


class ArticleDetailView(DetailView):
    model = models.Article
    template_name = 'article_details_2.html'


class ArticleUpdateView(UpdateView):
    model = models.Article
    fields = ['body']
    template_name = 'article_edit.html'


class ArticleDeleteView(DeleteView):
    model = models.Article
    template_name = 'article_delete_2.html'
    success_url = reverse_lazy('table')


class ArticleReclassify(UpdateView):
    model = models.Article
    fields = ['reclassification']
    template_name = 'article_reclassify.html'



def article_upload(request):
    template = 'article_upload.html'

    prompt = {
        'prompt':'Hello there...'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        return HttpResponseRedirect('/articles/error')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=','):
        _, created = models.Article.objects.update_or_create(
            body=column[0],
            source='csv')

    context = {}

    return HttpResponseRedirect('table') #render(request, template, context)

def article_download(request):

    items = models.Article.objects.all()

    response = HttpResponse(content_type = 'text/csv')

    response['Content-Disposition'] = 'attachment; filename="defects.csv"'

    writer = csv.writer(response, delimiter =',')
    writer.writerow(['Body', 'Classification'])

    for obj in items:
        writer.writerow([obj.body, obj.classification])

    return response


import json
from django.db.models import Count, Q
from django.shortcuts import render

def graph_view(request):
    dataset = models.Article.objects \
        .values('classification') \
        .annotate(true_count=Count('classification', filter=Q(reclassification__icontains = 'Not')),
                  total_count=Count('classification')) \
        .order_by('total_count')

    classification_list = list()
    #true_count_list = list()
    total_count_list = list()

    for entry in dataset:
        classification_list.append(entry['classification'])
        #true_count_list.append(entry['true_count'])
        total_count_list.append(entry['total_count'])

    '''true_series = {
        'name': 'Actual Count',
        'data': true_count_list,
        'color': 'green'
    }'''

    total_series = {

        'data': total_count_list,
        'colorByPoint': True,
        'showInLegend': False,

    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Defect Classification Analysis'},
        'xAxis': {'categories': classification_list},
        'series': [total_series],
    }


    dump = json.dumps(chart)

    return render(request, 'graph.html', {'chart': dump})