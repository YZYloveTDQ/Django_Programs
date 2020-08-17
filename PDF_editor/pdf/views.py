from django.shortcuts import render

# Create your views here.
from django.http import FileResponse, HttpResponse
from .forms import pdf_extract_form, pdf_merge_form, pdf_replace_form
import os
import PyPDF2
import zipfile


def pdf_single_page_extract(request):
    """PDF单页提取"""
    # 判断是否是通过post提交的表单
    if request.method == 'POST':
        form = pdf_extract_form(request.POST, request.FILES)

        # 判断表单是否有效
        if form.is_valid():
            # 提取表单文件
            f = form.cleaned_data['pdf']
            # 转化为PDF对象
            #pdf_object = PyPDF2.PdfFileReader(f)

            # 获取需提取页面页码，可能输入很多，所以自动存在列表中
            page_list = form.cleaned_data['page'].split(
                ',')  # 数据存储在cleaned_data

            # 创建压缩对象
            zip_file = zipfile.ZipFile(os.path.join(
                'media', 'extracted_pages.zip'), 'w')

            with open(os.path.join('media', 'original_pdf.pdf'), 'wb+') as pdf_object:
                for chunk in f.chunks():
                    pdf_object.write(chunk)

                pdf_reader = PyPDF2.PdfFileReader(pdf_object)

                for page in page_list:
                    page_index = int(page) - 1  # 对象索引是从0开始的

                    # 利用PyPDF2提取页码对应的页面对象
                    page_object = pdf_reader.getPage(page_index)

                    # 创建新的pdf writer
                    pdf_writer = PyPDF2.PdfFileWriter()
                    # 添加已经读取的页码对象
                    pdf_writer.addPage(page_object)

                # 提取的页面生成的PDF文件所存储的路径
                pdf_file_path = os.path.join(
                    'media', 'extracted_page_{}.pdf'.format(page))
                # 提取的页面写入到新的PDF文件中
                with open(pdf_file_path, 'wb') as f_output:
                    pdf_writer.write(f_output)

                # 将PDF文件写入zip文件
                zip_file.write(pdf_file_path)
            zip_file.close()

            # 给用户返回zip压缩包
            response = FileResponse(
                open(os.path.join('media', 'extracted_pages.zip'), 'rb'), content_type='application/octet-stream')
            #response['content-type'] = 'application/zip'
            response['Content-Disposition'] = "attachment;filename='extracted_pages.zip'"
            return response

    else:
        # 没有通过post提交
        form = pdf_extract_form()

    return render(request, 'pdf/pdf_extract.html', {'form': form})


def pdf_range_extract(request):
    """页面按范围提取"""
    if request.method == 'POST':
        form = pdf_extract_form(request.POST, request.FILES)

        if form.is_valid():

            # 获取上传的文件
            f = form.cleaned_data['pdf']
            # 提取的文件转化为PDF对象
            pdf_object = PyPDF2.PdfFileReader(f)

            # 获取页面范围，获取后自动存储于一个列表
            page_range = form.cleaned_data['page'].split('-')  # 获取两端数字
            page_start = int(page_range[0])
            page_end = int(page_range[1])

            # 提取页面后写入的PDF文件存储的位置路径
            pdf_file_path = os.path.join(
                'media', 'extracted_page_{}-{}.pdf'.format(page_start, page_end))

            # 输出的PDF文件
            # pdf_output_file = open(pdf_file_path, 'ab+')

            # 创建新的pdf writer
            pdf_writer = PyPDF2.PdfFileWriter()

            for page in range(page_start, page_end):
                page_index = page-1  # 对象索引是从0开始

                # 提取页码对应的页面对象
                page_object = pdf_object.getPage(page_index)

                # 添加已读取的页面对象
                pdf_writer.addPage(page_object)

            with open(pdf_file_path, 'wb') as f_output:
                pdf_writer.write(f_output)

            # 返回给用户
            response = FileResponse(open(pdf_file_path, 'rb'))
            response['content-type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="extracted_pages.pdf'

            return response
    else:
        form = pdf_extract_form()

    return render(request, 'pdf/pdf_range_extract.html', {'form': form})


def pdf_merge(request):
    """PDF合并"""
    if request.method == 'POST':
        form = pdf_merge_form(request.POST, request.FILES)

        if form.is_valid():
            # 获取上传的文件
            f1 = form.cleaned_data['pdf1']
            f2 = form.cleaned_data['pdf2']
            f3 = form.cleaned_data['pdf3']
            f4 = form.cleaned_data['pdf4']
            f5 = form.cleaned_data['pdf5']

            f_list = [f1, f2, f3, f4, f5]

            # 创建PDF合并对象
            pdf_merger = PyPDF2.PdfFileMerger()

            # 将提取的文件转化为PDF文件对象
            for f in f_list:
                if f:
                    pdf_object = PyPDF2.PdfFileReader(f)
                    pdf_merger.append(pdf_object)

            # 将合并对象写入一个新的PDF文件
            with open(os.path.join('media', 'merged_file.pdf'), 'wb') as f_output:
                pdf_merger.write(f_output)

            # 返回给用户
            response = FileResponse(
                open(os.path.join('media', 'merged_file.pdf'), 'rb'))
            response['content-type'] = 'application/pdf'
            response['Content-Disposition'] = "attachment;filename='merged_file.pdf'"

            return response
    else:
        form = pdf_merge_form()

    return render(request, 'pdf/pdf_merge.html', {'form': form})


def pdf_replace(request):
    """页面替换"""
    if request.method == 'POST':
        form = pdf_replace_form(request.POST, request.FILES)

        if form.is_valid():
            # 获取需要插入的PDF文件
            f1 = form.cleaned_data['pdf1']
            # 获取被插入文件
            f2 = form.cleaned_data['pdf2']
            # 获取替换页码
            page = form.cleaned_data['page']

            # 获取被插入文件的总页数
            pdf_object = PyPDF2.PdfFileReader()
            total_page = pdf_object.getNumPages()

            # 将被插入文件分成三个部分，以待插入页码为分界点

            # 第一部分
            page_start = 1
            page_end = page-1

            pdf_output1 = open(os.path.join('media', 'part1.pdf'), 'wb+')

            pdf_writer = PyPDF2.PdfFileWriter()

            for page_num in range(page_start, page_end+1):
                page_index = page_num-1

                # 一页页提取写入，先转化成对象
                page_object = pdf_object.getPage(page_index)
                pdf_writer.addPage(page_object)

            pdf_writer.write(pdf_output1)
            pdf_output1.close()

            # 第二部分
            page_start = page + 1
            page_end = total_page

            pdf_output2 = open(os.path.join('media', 'part2.pdf'), 'wb+')

            pdf_writer = PyPDF2.PdfFileWriter()

            for page_num in range(page_start, page_end):
                page_index = page_num-1

                # 一页页提取，先转化为对象
                page_object = pdf_object.getPage(page_index)
                pdf_writer.addPage(page_object)

            pdf_writer.write(pdf_output2)
            pdf_output2.close()

            # 创建合并对象
            pdf_merger = PyPDF2.PdfFileMerger()
            pdf_merger.append(open(os.path.join('media', 'part1.pdf'), 'rb+'))
            pdf_merger.append(PyPDF2.PdfFileReader(f1))
            pdf_merger.append(open(os.path.join('media', 'part2.pdf'), 'rb+'))

            # 将合并对象写入PDF文件
            with open(os.path.join('media', 'replaced_file.pdf'), 'wb') as f_output:
                pdf_merger.write(f_output)

            # 返回给用户
            response = FileResponse(
                open(os.path.join('media', 'replaced_file.pdf'), 'rb'))
            response['content-type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment;filename='replaced_file.pdf'"

            return response

    else:
        form = pdf_replace_form()

    return render(request, 'pdf/pdf_replace.html', {'form': form})
