from django import forms


class pdf_merge_upload(forms.Form):
    """上传2个pdf文件用于合并"""
    pdf1 = forms.FileField(label="上传的pdf文件1")
    pdf2 = forms.FileField(label="上传的pdf文件2")
