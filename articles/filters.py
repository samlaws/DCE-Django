import django_filters
from .models import Article, STATUS_CHOICES_CLASS, STATUS_CHOICES_SOURCE, classes
from django import forms

class ArticleFilter(django_filters.FilterSet):

    source = django_filters.ChoiceFilter(choices=STATUS_CHOICES_SOURCE)
    classification = django_filters.ChoiceFilter(choices=STATUS_CHOICES_CLASS)
    reclassification = django_filters.ChoiceFilter(choices = classes)
    body = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = Article
        fields = [ 'id', 'source', 'classification', 'reclassification', 'body']
