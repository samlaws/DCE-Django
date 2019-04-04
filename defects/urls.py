from django.urls import path
from . import views

urlpatterns = [
    path('new', views.DefectCreateView.as_view(), name='defect_new'),
    path('download', views.defect_download, name = 'download'),
    path('upload', views.defect_upload, name = 'upload'),
    path('error', views.FileError.as_view(), name = 'error'),
    path('<int:pk>/edit/', views.DefectUpdateView.as_view(), name='defect_edit'), # new
    path('<int:pk>/', views.DefectDetailView.as_view(), name='defect_detail'), # new
    path('<int:pk>/delete/', views.DefectDeleteView.as_view(), name='defect_delete'),
    path('table', views.FilteredDefectListView.as_view(), name='table'),
    path('<int:pk>/reclassify/', views.DefectReclassify.as_view(), name='defect_reclassify'),
    path('graph/bar/', views.bar_graph_view, name='bar_chart'),
    path('graph/sidebar/', views.sideways_graph_view, name='side_chart'),
    path('graph/pie/', views.pie_graph_view, name='pie_chart'),
    path('graph/bar/daily/', views.daily_bar_view, name = 'daily_bar'),
    path('graph/bar/monthly/', views.monthly_bar_view, name = 'monthly_bar'),
    path('graph', views.GraphPage.as_view(), name = 'graphs'),
]
