import django_tables2 as tables
from django_tables2 import TemplateColumn, Column, DateTimeColumn
from . import models
from .classifier import classify_defect

class ArticleTable(tables.Table):
    id = Column(initial_sort_descending=True)
    #body_str = Column(verbose_name='Classification', order_by=('id'))
    #date = DateTimeColumn(format='d-m-y H:i', )
    detail = TemplateColumn(template_name='training_update_column.html')
    delete = TemplateColumn(template_name='training_delete_column.html')
    reclassify = TemplateColumn(template_name = 'training_reclassify_column.html')


    class Meta:
        model = models.Article

        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'body', 'source', 'classification', 'date', 'detail', 'delete', 'reclassify', 'reclassification')
        attrs={'td': {'bgcolor': '#F3F3EE'},
            'th': {'bgcolor': '#61615F'},
            'tf': {'color': '#F3F3EE'}
            }
