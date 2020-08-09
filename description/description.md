# 项目：PDF 单页提取

> 由于只是一个应用功能的实现，所以涉及不到模型的涉及

---

## 【1】项目描述

设计一个表单，用户上传 PDF 文件和输入要提取单页的页码。服务器收到表单后，使用**PyPDF2**库读取用户上传的 PDF 文件，提取所需的页码,通过 HTTPResponse 将这个新生成的 PDF 文件返回给用户

---

## 【2】表单的设计 forms.py

**两个字段：**

1. pdf_file：用户选择要上传的文件
2. page：用户输入要提取的页面页码
   （对于自定义 forms.Form，==label==属性用于描述该字段）

**注意**：表单的设计，使用的是==class==

---

## 【3】视图函数 views.py

PyPDF2 可以提取 pdf 文件里的文字，也可以抓取 pdf 文件中的某个页面，还可以创建新的 pdf 文件

**视图函数编写：**

1. 判断是否通过==post==提交了表单，若没有则只能创建空表单
```python
if request.method == "POST":
        form = pdf_upload(request.POST, request.FILES)
```
**request.FILES**：Django中用于文件上传时使用的参量，这是一个==字典==，其中包含了表单的每个==字段==。且它只有在请求方法为==post==时才有效
```python
request.FILES['字段名'] # 访问对应字段的对象
```

2. 需要判断表单是否有效
```python
if form.is_valid():  # 判断表单是否有效
```

3. ==判断是否是pdf文件==
获取上传文件的文件名，以"."为拆分点，获取后缀名，判断是否是"pdf"
```python
filename, file_type = f.name.split('.')
            if file_type != 'pdf':
                return render(request, 'pdf/not_pdf.html')
```
**request.FILES['字段名'].name**可以直接获取字段名

**注意**：写明路由时，一定要写仔细

**对应的not_pdf.html:**
```html
{% block content %}
<p>上传文件类型错误！</p>
<a href="{% url 'pdf: pdf_extract' %}">返回提取页面</a>
{% endblock %}
```
==一定要写明命名空间==

4. 对于上传的pdf进行操作前，先将其写入到一个新的文档中，避免对原文档进行操作
> 利用 ==chunk（块）== 进行读写，避免大文件占用过多内存
```python
with open('original_pdf', 'wb+') as pdf_object:
                for chunk in f.chunks():  # 快式读写，效率更高
                    pdf_object.write(chunk)
```

5. 读写到新文档后，利用PyPDF2开始操作
```python
pdf_reader = PyPDF2.PdfFileReader(pdf_object)  # PyPDF2读取文件
pdf_page = pdf_reader.getPage(page_index)  # PyPDF2读取要提取的页面页码

pdf_writer = PyPDF2.PdfFileWriter()  # PyPDF2创建一个新的pdf对象
pdf_writer.addPage(pdf_page)  # PyPDF2提取的页面加入到新创建的pdf对象中
```

6. 将PyPDF2的pdf对象写道一个新的pdf文件中（待返回的文件）
```python
with open('extracted_page.pdf', 'wb') as f:
                f.write(pdf_writer)  # 将提取好的pdf对象写入一个新的pdf文件中
```

7. 返回提取好的pdf文件
```python
with open('extracted_page.pdf', 'rb') as f:
                response = HttpResponse(
                    f.read(), content_type='application/pdf')  # 说明返回类别，避免乱码
                response['content-Disposition'] = 'attachment;filename="extracted_page_{}.pdf"'.format(
                    pdf_page)
                return response
```
- ```content_type='application/pdf'```：用于说明类型，避免乱码
- ```response['content-Disposition']```：内容配置，说明==以何种形式==返回
    > 常规的HTTP响应中，**content-Disposition**指示回复的内容以何种形式展示
    > - **inline**：内联的形式（即网页）
    > - **attachment**：==附件的形式==，若没有设置filename则会呈现“保存为”对话框
    > - **attachment**；filename=''：设置了默认名字，则直接本地下载

8. 若没有使用post提交数据
```python
else:  # 没有通过post提交数据
        form = pdf_upload()  # 创建空表单
        return render(request, 'pdf/pdf_extract.html', {'form': form})
```

---
**pdf_upload.html**
```html
{% block content %}
<h3>上传PDF文件，输入要提取的页码</h3>
<form method='post' enctype='multipart/form-data' action="">
    {% csrf_token %}
    {{ form.as_p }}
    <input type='submit' value='确定' />
</form>
{% endblock %}
```
- **enctype**即encodetype：编码类型
    - 默认：```application/x-www-form-urlencoded```：只能上传文本格式
    - ```multipart/form-data```：表单==多部份构成，既有文本也有二进制数据==，实现多类型文件上传
- **{% crsf_token %}**：防御crsf攻击，以参数形式加一个==随机token（令牌）==。若请求中没有这个token或不正确，则可能是crsf攻击
- **{{ form.as_p }}**：django以字段形式渲染表单所有元素，一种显示表单的简洁方法

---
## 【4】上传文件页数过大失效
读取上传文件后，利用**getNumPages()**
```python
# ====若上传文件页数太大则失效=================
if pdf_reader.getNumPages() > 10:
    return render(request, 'pdf/too_large.html')
```

---
**注意：** 模板中的url是指向的视图views中的函数，不是html模板（即是要跳到调用模板html的地方）