from django.views.generic import ListView, CreateView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
import csv
from datetime import datetime
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from . import models
import io
from .tables import DefectTable
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import DefectFilter
import json
from django.db.models import Count, Q
from django_tables2.export.views import ExportMixin


class FilteredDefectListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = DefectTable
    model = models.Defect
    template_name = 'table.html'
    export_name = 'Defect Data ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    exclude_columns = ('id', 'detail', 'delete', 'reclassify')

    filterset_class = DefectFilter


class DefectCreateView(CreateView):
    model = models.Defect
    template_name = 'defect_new.html'
    fields = ['body']


class FileError(TemplateView):
    model = models.Defect
    template_name = 'error.html'


class DefectDetailView(UpdateView):
    model = models.Defect
    fields = ['reclassification']
    template_name = 'defect_details.html'


class DefectUpdateView(UpdateView):
    model = models.Defect
    fields = ['body']
    template_name = 'defect_edit.html'


class DefectDeleteView(DeleteView):
    model = models.Defect
    template_name = 'defect_delete.html'
    success_url = reverse_lazy('table')


class DefectReclassify(UpdateView):
    model = models.Defect
    fields = ['reclassification']
    template_name = 'defect_reclassify.html'


def defect_upload(request):
    template = 'defect_upload.html'

    prompt = {
        'prompt':'Hello there...'
    }

    if request.method == 'GET':
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        return HttpResponseRedirect('/defects/error')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=','):
        _, created = models.Defect.objects.update_or_create(
            body=column[0],
            source='csv')

    context = {}

    return HttpResponseRedirect('table') #render(request, template, context)


def defect_download(request):

    items = models.Defect.objects.all()

    response = HttpResponse(content_type = 'text/csv')

    response['Content-Disposition'] = 'attachment; filename="defects.csv"'

    writer = csv.writer(response, delimiter =',')
    writer.writerow(['Body', 'Source', 'Classification', 'Reclassification', 'Date'])

    for obj in items:
        writer.writerow([obj.body, obj.source, obj.classification, obj.reclassification, obj.date])

    return response


def bar_graph_view(request):

    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(total_count=Count('classification')) \
        .order_by('-total_count')

    classification_list = list()
    total_count_list = list()

    for entry in dataset:
        classification_list.append(entry['classification'])
        total_count_list.append(entry['total_count'])

    total_series = {
        'data': total_count_list,
        'colorByPoint': True,
        'showInLegend': False,
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Defect Classification Analysis - Bar Chart'},
        'xAxis': {'categories': classification_list},
        'series': [total_series],
    }

    dump = json.dumps(chart)
    return render(request, 'graph.html', {'chart': dump})

def sideways_graph_view(request):

    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(total_count=Count('classification')) \
        .order_by('-total_count')

    classification_list = list()
    total_count_list = list()

    for entry in dataset:
        classification_list.append(entry['classification'])
        total_count_list.append(entry['total_count'])

    total_series = {

        'data': total_count_list,
        'colorByPoint':True,
        'showInLegend': False,
    }

    chart = {
        'chart': {'type': 'bar'},
        'title': {'text': 'Defect Classification Analysis - Side Bar'},
        'xAxis': {'categories': classification_list},
        'series': [total_series],
    }

    dump = json.dumps(chart)
    return render(request, 'graph.html', {'chart': dump})

def pie_graph_view(request):

    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(total_count=Count('classification')) \
        .order_by('-total_count')

    display_name = dict()

    for tuple in models.CLASSES:
        display_name[tuple[0]] = tuple[1]

    chart = {
        'chart': {'type':'pie'},
        'title':{'text':'Defect Classification Analysis - Pie Chart'},
        'series':[{
            'data': list(map(lambda row: {'name': display_name[row['classification']], 'y': row['total_count']}, dataset))
        }]
    }

    dump = json.dumps(chart)
    return render(request, 'graph.html', {'chart': dump})

