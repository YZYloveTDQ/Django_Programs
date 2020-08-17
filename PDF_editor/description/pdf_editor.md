# PDF 编辑器

主要包含四个概念模块：

- PDF 单页提取
- PDF 按范围提取
- PDF 文件合并
- PDF 单页替换

利用==Django 框架 + PyPDF2 库==开发一个使用的小应用程序，服务于我的==随米打印业务==

---

## 【1】PDF 单页提取和按范围提取

单页提取和按范围提取的表单是一个，只不过在输入页面页码时有区别
用户上传一个 PDF 文件，输入要提取的页码，服务器收到后利用 PyPDF2 库提取用户上传的 PDF，提取所需的页面页码

- 单页提取的页码：用逗号隔开（可以同时提取多个）
- 按范围提取的页码：利用“-”代表范围
  单页提取后的文件用==zipfile==库压缩成一个压缩文件返回给用户

#### 【1.1】单页提取

用户上传 PDF 文件和一连串用逗号隔开的数字

- 先使用==split()== 取出数字
- 依次利用 PyPDF2 取出对应页面，单页写入 PDF 文件，存储 media 文件夹
- 利用==zipfile== 库将所有写入的 pdf 文件压缩成 zip
- 通过==FileResponse== 返回给用户

由于可以提取多个页面，输入的页码是利用逗号隔开的，所以表单中页码的字段使用==forms.Charfield==

**在表单中直接对某个字段进行检测**：

```python
def clean_pdf(self):
        """检测pdf字段"""
        pdf = self.cleaned_data.get('pdf')
        if not pdf.name.lower().endswith('.pdf'):  # 检测后缀是否是pdf
            raise forms.ValidationError("上传文件格式错误")

        return pdf
```

创建**clean\_字段名()**函数

- 表单中的数据是存储在**cleaned_data**中的

获取某个字段数据可以通过两种方式

```python
request.FILES[字段名]
form.cleaned_data[字段名]
```

---

## 【2】PDF 页面合并

输入多个文件

PyPDF2 的 PdfFileMerger()需要==先创建对象，然后 append==

## 【3】PDF 单页替换

- 被替换 PDF 文件
- 替换的 pdf 文件（只有一页）
- 替换页面页码

**思路**：

1. 被插入 pdf 文件拆分成三部分：==替换页面前 part、被替换页、替换页面后 part==
2. 然后将==替换页面前 part==与==替换 pdf 文件==与==替换页面后 part==进行合并

---

1. **static**文件夹包含四个子文件夹：js、fonts、images、css

   > 用于存储静态文件，梅花页面

2. **media**文件夹：存放上传的文件

   > 所以每次都需要使用**os.path.join('media', 设置文件名)**

3. 浏览器检测文件类型时有两种响应：
   1. MIME：多功能 Internet 邮件扩充服务，最早用于邮件系统
   2. 'application/octet-stream'：无法确定文件类型时使用

---

项目部署在**pythonanywhere 平台**上

> 部署过程中要注意虚拟环境的设置，安装对应安装包

---

# 项目问题

**一直无法下载文件，刚开始以为是 HTTPResponse 错误，更换成了其他返回形式，FileResponse，后来查了很多资料，知乎、微信、stackoverflow 开源中国……**

==发现是 post 问题，判断是空表单了==

```python
if request.method == 'POST'
```

POST 一定要大写
