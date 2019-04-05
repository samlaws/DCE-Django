from django.views.generic import ListView, CreateView, TemplateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
import csv
import datetime as dt
from datetime import datetime
from django.shortcuts import HttpResponse, render, HttpResponseRedirect
from . import models
import io
from .tables import DefectTable
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import DefectFilter, GraphFilter
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
        'prompt': 'Hello there...'
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

    return HttpResponseRedirect('table')


def defect_download(request):

    items = models.Defect.objects.all()

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename="defects.csv"'

    writer = csv.writer(response, delimiter=',')
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
        'name': 'Defects',
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
        'name': 'Total Defects',
        'data': total_count_list,
        'colorByPoint': True,
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
        'chart': {'type': 'pie'},
        'title': {'text': 'Defect Classification Analysis - Pie Chart'},
        'series': [{'name': 'Defects',
                    'data': list(map(lambda row: {'name': display_name[row['classification']],
                                                  'y': row['total_count']}, dataset))
                    }]
    }

    dump = json.dumps(chart)
    return render(request, 'graph.html', {'chart': dump})


def daily_bar_view(request):

    today_min = datetime.combine(datetime.now(), dt.time.min)
    today_max = datetime.combine(datetime.now(), dt.time.max)

    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(daily_count=Count('classification', filter=Q(date__range = (today_min, today_max)))) \
        .order_by('-daily_count')

    classification_list = list()
    daily_count_list = list()

    for entry in dataset:
        classification_list.append(entry['classification'])
        daily_count_list.append(entry['daily_count'])

    daily_series = {
        'name': 'Defects',
        'data': daily_count_list,
        'colorByPoint': True,
        'showInLegend': False,
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Defect Classification Analysis - Bar Chart'},
        'xAxis': {'categories': classification_list},
        'series': [daily_series],
    }

    dump = json.dumps(chart)
    return render(request, 'daily_graph.html', {'chart': dump})


def daily_side_view(request):

    today_min = datetime.combine(datetime.now(), dt.time.min)
    today_max = datetime.combine(datetime.now(), dt.time.max)

    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(daily_count=Count('classification', filter=Q(date__range = (today_min, today_max)))) \
        .order_by('-daily_count')

    classification_list = list()
    daily_count_list = list()

    for entry in dataset:
        classification_list.append(entry['classification'])
        daily_count_list.append(entry['daily_count'])

    daily_series = {
        'name': 'Defects',
        'data': daily_count_list,
        'colorByPoint': True,
        'showInLegend': False,
    }

    chart = {
        'chart': {'type': 'bar'},
        'title': {'text': 'Defect Classification Analysis - Bar Chart'},
        'xAxis': {'categories': classification_list},
        'series': [daily_series],
    }

    dump = json.dumps(chart)
    return render(request, 'daily_graph.html', {'chart': dump})


def daily_pie_view(request):

    today_min = datetime.combine(datetime.now(), dt.time.min)
    today_max = datetime.combine(datetime.now(), dt.time.max)

    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(daily_count=Count('classification', filter=Q(date__range = (today_min, today_max)))) \
        .order_by('-daily_count')

    display_name = dict()

    for tuple in models.CLASSES:
        display_name[tuple[0]] = tuple[1]

    chart = {
        'chart': {'type':'pie'},
        'title':{'text':'Defect Classification Analysis - Pie Chart'},
        'series':[{'name': 'Defects',
            'data': list(map(lambda row: {'name': display_name[row['classification']], 'y': row['daily_count']}, dataset))
        }]
    }

    dump = json.dumps(chart)
    return render(request, 'daily_graph.html', {'chart': dump})


def monthly_bar_view(request):

    today = datetime.now()


    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(month_count=Count('classification', filter=Q(date__month=today.month) | Q(date__year=today.year))) \
        .order_by('-month_count')

    classification_list = list()
    month_count_list = list()

    for entry in dataset:
        classification_list.append(entry['classification'])
        month_count_list.append(entry['month_count'])

    month_series = {
        'name': 'Defects',
        'data': month_count_list,
        'colorByPoint': True,
        'showInLegend': False,
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Defect Classification Analysis - Bar Chart'},
        'xAxis': {'categories': classification_list},
        'series': [month_series],
    }

    dump = json.dumps(chart)
    return render(request, 'monthly_graph.html', {'chart': dump})


def monthly_side_view(request):

    today = datetime.now()


    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(month_count=Count('classification', filter=Q(date__month=today.month))) \
        .order_by('-month_count')

    classification_list = list()
    month_count_list = list()

    for entry in dataset:
        classification_list.append(entry['classification'])
        month_count_list.append(entry['month_count'])

    month_series = {
        'name': 'Defects',
        'data': month_count_list,
        'colorByPoint': True,
        'showInLegend': False,
    }

    chart = {
        'chart': {'type': 'bar'},
        'title': {'text': 'Defect Classification Analysis - Bar Chart'},
        'xAxis': {'categories': classification_list},
        'series': [month_series],
    }

    dump = json.dumps(chart)
    return render(request, 'monthly_graph.html', {'chart': dump})


def monthly_pie_view(request):

    today = datetime.now()

    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(month_count=Count('classification', filter=Q(date__month = today.month))) \
        .order_by('-month_count')

    display_name = dict()

    for tuple in models.CLASSES:
        display_name[tuple[0]] = tuple[1]

    chart = {
        'chart': {'type':'pie'},
        'title':{'text':'Defect Classification Analysis - Pie Chart'},
        'series':[{'name': 'Defects',
            'data': list(map(lambda row: {'name': display_name[row['classification']], 'y': row['month_count']}, dataset))
        }]
    }

    dump = json.dumps(chart)
    return render(request, 'monthly_graph.html', {'chart': dump})


def stacked_bar_view(request):

    dataset = models.Defect.objects \
        .values('classification') \
        .annotate(csv_count=Count('classification', filter = Q(source__iexact = 'csv')),
                  entry_count = Count('classification', filter = Q(source__iexact = 'Entry'))
                  ) \
        .order_by('-csv_count')

    category_list = list()
    csv_list = list()
    entry_list = list()

    for entry in dataset:
        category_list.append(entry['classification'])
        csv_list.append(entry['csv_count'])
        entry_list.append(entry['entry_count'])

    csv_series = {
        'name': 'CSV File',
        'data': csv_list,
    }

    entry_series = {
        'name': 'Entry',
        'data': entry_list,
    }

    chart  = {
        'chart': {'type': 'bar'},
        'title': {'text': 'Defect Classification Analysis - Bar Chart'},
        'xAxis': {'categories': category_list},
        'plotOptions': {'series': {'stacking': 'normal', 'dataLabels': {'enabled':False}}},
        'series': [csv_series, entry_series],
        'yAxis': {'title': {'text': 'Number of Classified Defects'}, 'stackLabels': {'enabled':True, 'style': {'fontWeight':'bold'}}},
        'tooltip': {'headerFormat': '<b>{point.x}</b><br/>', 'pointFormat': '{series.name}: {point.y}<br/>Total: {point.stackTotal}'}
    }

    dump = json.dumps(chart)
    return render(request, 'graph.html', {'chart': dump})

class GraphPage(TemplateView):
    model = models.Defect
    template_name = 'graph_page.html'
