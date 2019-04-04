import django_filters
from .models import Article, STATUS_CHOICES_CLASS, STATUS_CHOICES_SOURCE, classes
from django import forms

class ArticleFilter(django_filters.FilterSet):

    source = django_filters.ChoiceFilter(choices=STATUS_CHOICES_SOURCE, empty_label = 'Source')
    classification = django_filters.ChoiceFilter(choices=STATUS_CHOICES_CLASS, empty_label = 'Classification')
    reclassification = django_filters.ChoiceFilter(choices = classes, empty_label = 'Reclassification')
    body = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = Article
        fields = ['source', 'classification', 'reclassification', 'body']
