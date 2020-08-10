from django.shortcuts import render
from .forms import pdf_upload, pdf_merge_upload
from django.http import HttpResponse
import PyPDF2


def pdf_merge(request):
    """合并两个pdf文件"""
    # 先判断是否是通过post上传的表单
    if request.method == "post":
        form = pdf_merge_upload(request.POST, request.FILES)

        # 判断表单是否有效
        if form.is_valid():
            # 获取上传的文件
            f1 = request.FILES['pdf1']
            f2 = request.FILES['pdf2']

            # 将两个文件转化为PDF文件对象
            pdf_object1 = PyPDF2.PdfFileReader(f1)
            pdf_object2 = PyPDF2.PdfFileReader(f2)

            # 创建PDF合并对象，合并这两个对象
            pdf_merger = PyPDF2.PdfFileMerger()  # 创建pdf合并文件
            pdf_merger.append(pdf_object1)
            pdf_merger.append(pdf_object2)

            # 将合并对象写入一个merged_file.pdf
            with open('merged_pdf.pdf', 'wb') as f:
                pdf_merger.write(f)

            # 打开合并的pdf文件，返回
            with open('merged_pdf.pdf', 'rb') as f:
                response = HttpResponse(
                    f.read(), content_type='application/pdf')  # 避免乱码
                # 附件形式返回
                response['Content-Disposition'] = 'attachment;filename="merged_pdf.odf"'
                return response

        else:  # 表单未通过验证
            form = pdf_merge_upload()

    else:  # 未通过post提交
        form = pdf_merge_upload()  # 空表单

    return render(request, 'pdf/pdf_merge.html', {'form': form})
