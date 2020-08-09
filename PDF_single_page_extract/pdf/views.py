from django.shortcuts import render
from .forms import pdf_upload
from django.http import HttpResponse
import PyPDF2

# Create your views here.


def pdf_extract(request):
    """PDF文件单页提取"""
    if request.method == "POST":  # 是否是通过post提交的表单
        form = pdf_upload(request.POST, request.FILES)  # 是则创建表单，获取上传的数据

        if form.is_valid():  # 判断表单是否有效
            # 将上传的数据提取出来
            page_number = int(request.POST.get('page'))  # 获取要提取页面页码
            page_index = page_number - 1  # PyPDF2对文档处理索引也是从0开始
            f = request.FILES['pdf_file']  # 获取上传的pdf文件

            # ----判断是否是pdf文件--------------------------
            filename, file_type = f.name.split('.')  # 获取文件名后缀
            if file_type != 'pdf':
                return render(request, 'pdf/not_pdf.html')

            # 将上传的文件读写到一个新的pdf文件中
            with open('original_pdf', 'wb+') as pdf_object:  # 二进制读写模式
                for chunk in f.chunks():  # 快式读写，效率更高
                    pdf_object.write(chunk)

                # ------利用PyPDF2进行操作-----------------------------
                pdf_reader = PyPDF2.PdfFileReader(pdf_object)  # PyPDF2读取文件

                # ====若上传文件页数太大则失效=================
                if pdf_reader.getNumPages() > 1000000:
                    return render(request, 'pdf/too_large.html')
                # =========================================

                pdf_page = pdf_reader.getPage(page_index)  # PyPDF2读取要提取的页面页码

                pdf_writer = PyPDF2.PdfFileWriter()  # PyPDF2创建一个新的pdf对象
                pdf_writer.addPage(pdf_page)  # PyPDF2提取的页面加入到新创建的pdf对象中

                # ----------------------------------------------------
                with open('extracted_page.pdf', 'wb') as f1:  # 二进制写模式
                    pdf_writer.write(f1)  # 将提取好的pdf对象写入一个新的pdf文件中

                # ---------准备返回提取好的pdf文件-----------------
                with open('extracted_page.pdf', 'rb') as f2:  # 二进制读模式
                    response = HttpResponse(
                        f2.read(), content_type='application/pdf')  # 说明返回类别，避免乱码
                    response['content-Disposition'] = 'attachment;filename="extracted_page_{}.pdf"'.format(
                        pdf_page)
                    return response
    else:  # 没有通过post提交数据
        form = pdf_upload()  # 创建空表单
        return render(request, 'pdf/pdf_upload.html', {'form': form})
