import django_tables2 as tables
from django_tables2 import TemplateColumn, Column, DateTimeColumn
from . import models
from django.utils.safestring import mark_safe


class DivWrappedColumn(tables.Column):

    def __init__(self, classname=None, *args, **kwargs):
        self.classname=classname
        super(DivWrappedColumn, self).__init__(*args, **kwargs)

    def render(self, value):
        return mark_safe("<div class='" + self.classname + "' >" +value+"</div>")



class ArticleTable(tables.Table):

    export_formats = ['csv']

    id = Column(initial_sort_descending=True)
    #body_str = Column(verbose_name='Classification', order_by=('id'))
    #date = DateTimeColumn(format='d-m-y H:i', )
    detail = TemplateColumn(template_name='training_update_column.html')
    delete = TemplateColumn(template_name='training_delete_column.html')
    reclassify = TemplateColumn(template_name = 'training_reclassify_column.html')



    class Meta:
        model = models.Article
        order_by = '-id'
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'body', 'source', 'classification', 'reclassification', 'date', 'detail', 'delete', 'reclassify')
        attrs={'td': {'bgcolor': '#F3F3EE'},
            'th': {'bgcolor': '#61615F'},
            'tf': {'color': '#F3F3EE'},

            }

    def render_body(self, value):
        return value