# 自定义库：render.py
# 作用：利用docxtpl库渲染带有图片的模板文件

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import base64
import tempfile
import urllib.parse

def render_docx(readpath, savepath, data):
    doc = DocxTemplate(readpath) #加载模板文件

    # 图片处理（base64）
    for key in data.keys():
        if 'img' in key or 'image' in key:
            tmp_file = tempfile.NamedTemporaryFile(delete=None, suffix='.jpg')

            img_blob = base64.urlsafe_b64decode(urllib.parse.unquote(data[key]).split('base64,')[1])

            tmp_file.write(img_blob)
            tmp_file.close()

            print(tmp_file.name)
            
            data[key] = InlineImage(doc, tmp_file.name, width=Mm(60))

    doc.render(data) #填充数据
    doc.save(savepath) #保存目标文件
