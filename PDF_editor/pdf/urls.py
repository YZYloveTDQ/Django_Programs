from django.urls import path
from . import views

# 命名空间
app_name = 'pdf'

urlpatterns = [
    # 单页提取
    path('extract/single/', views.pdf_single_page_extract, name='pdf_single_page_extract'),

    # 范围提取
    path('extract/range/', views.pdf_range_extract, name='pdf_range_extract'),

    # 合并
    path('merge/', views.pdf_merge, name='pdf_merge'),

    # 页面替换
    path('replace/', views.pdf_replace, name='pdf_replace'),
]