from django import forms


class pdf_extract_form(forms.Form):
    """页面提取表单"""
    pdf = forms.FileField(label="上传PDF文件")
    page = forms.CharField(max_length=20, label="选择提取页面页面")

    def clean_pdf(self):
        """检测pdf字段"""
        pdf = self.cleaned_data.get('pdf')
        if not pdf.name.lower().endswith('.pdf'):  # 检测后缀是否是pdf
            raise forms.ValidationError("上传文件格式错误")

        return pdf


class pdf_merge_form(forms.Form):
    """pdf合并表单"""
    pdf1 = forms.FileField(label="上传的PDF文件1")
    pdf2 = forms.FileField(label="上传的PDF文件2")
    pdf3 = forms.FileField(label="上传的PDF文件3")
    pdf4 = forms.FileField(label="上传的PDF文件4")
    pdf5 = forms.FileField(label="上传的PDF文件5")


class pdf_replace_form(forms.Form):
    """PDF页面替换表单"""
    pdf1 = forms.FileField(label="上传替换的PDF文件")
    pdf2 = forms.FileField(label="上传被替换的页面文件")  # 替换的页面也是一个pdf文件，只有一页
    page = forms.IntegerField(label="替换的页面页码")
