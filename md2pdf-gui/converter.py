import markdown
import os
from weasyprint import HTML, CSS

class MarkdownConverter:
    HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Markdown PDF</title>
</head>
<body>
    {content}
</body>
</html>"""
    
    def __init__(self, css_path=None):
        if css_path is None:
            # 默认使用同目录下的styles/github.css
            base_dir = os.path.dirname(os.path.abspath(__file__))
            css_path = os.path.join(base_dir, 'styles', 'github.css')
        
        self.css_path = css_path if os.path.exists(css_path) else None
        
    def convert_file(self, input_path, output_path):
        """将markdown文件转换为PDF"""
        # 验证输入文件
        if not os.path.exists(input_path):
            return False, f"文件不存在: {input_path}"
        
        if not input_path.endswith('.md'):
            return False, "请输入markdown文件(.md)"
        
        try:
            # 读取markdown文件
            with open(input_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            if not md_content.strip():
                return False, "文件内容为空"
            
            # 转换为HTML
            html_content = self._markdown_to_html(md_content)
            
            # 生成PDF
            self._html_to_pdf(html_content, output_path)
            
            # 验证输出文件
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return True, f"PDF已保存: {output_path}"
            else:
                return False, "PDF生成失败，输出文件无效"
                
        except UnicodeDecodeError:
            return False, "文件编码错误，请确保文件为UTF-8编码"
        except (IOError, OSError) as e:
            return False, f"文件读写错误: {str(e)}"
        except Exception as e:
            return False, f"转换失败: {str(e)}"
    
    def _markdown_to_html(self, md_content):
        """将markdown转换为HTML"""
        extensions = [
            'extra',
            'codehilite',
            'toc',
            'nl2br',
            'sane_lists',
        ]
        
        html = markdown.markdown(md_content, extensions=extensions)
        
        return self.HTML_TEMPLATE.format(content=html)
    
    def _html_to_pdf(self, html_content, output_path):
        """将HTML转换为PDF"""
        try:
            if self.css_path and os.path.exists(self.css_path):
                css = CSS(filename=self.css_path)
                HTML(string=html_content).write_pdf(output_path, stylesheets=[css])
            else:
                HTML(string=html_content).write_pdf(output_path)
        except Exception as e:
            raise Exception(f"PDF生成失败: {str(e)}")
