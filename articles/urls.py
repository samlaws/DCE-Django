from django.urls import path
from . import views

urlpatterns = [
    #path('', views.ArticleListView.as_view(), name='article_list'),
    path('new', views.ArticleCreateView.as_view(), name='article_new'),
    path('download', views.article_download, name = 'download'),
    path('upload', views.article_upload, name = 'upload'),
    path('error', views.FileError.as_view(), name = 'error'),
    path('<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'), # new
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'), # new
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('table', views.FilteredArticleListView.as_view(), name='table'),
    path('<int:pk>/reclassify/', views.ArticleReclassify.as_view(), name='article_reclassify'),
]
