from django import forms


class pdf_upload(forms.Form):
    """上传PDF的表单"""
    pdf_file = forms.FileField(label="选择要上传的pdf文件")
    page = forms.IntegerField(min_value=1, label="选择要提取的页面页码")
