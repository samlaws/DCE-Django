import django_filters
from .models import Article, STATUS_CHOICES_CLASS, STATUS_CHOICES_SOURCE
from django import forms

class ArticleFilter(django_filters.FilterSet):

    source = django_filters.ChoiceFilter(choices=STATUS_CHOICES_SOURCE)
    classification = django_filters.ChoiceFilter(choices=STATUS_CHOICES_CLASS)


    class Meta:
        model = Article
        fields = [ 'id', 'source', 'classification',]
