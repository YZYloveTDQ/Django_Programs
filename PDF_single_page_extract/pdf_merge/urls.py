from django.urls import path
from . import views

# 命名空间
app_name = 'pdf'

urlpatterns = [
    path('extract/', views.pdf_extract, name='pdf_extract'),
    path('merge/', views.pdf_merge, name='pdf_merge'),
]
