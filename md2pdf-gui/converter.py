import markdown
import os

# 延迟导入weasyprint，避免在Windows上因缺少GTK库而无法导入
_html_converter = None
_css_converter = None

def _get_weasyprint():
    global _html_converter, _css_converter
    if _html_converter is None:
        from weasyprint import HTML, CSS
        _html_converter = HTML
        _css_converter = CSS
    return _html_converter, _css_converter

class MarkdownConverter:
    def __init__(self, css_path=None):
        self.css_path = css_path
        
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
        
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Markdown PDF</title>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        return full_html
    
    def _html_to_pdf(self, html_content, output_path):
        """将HTML转换为PDF"""
        try:
            HTML, CSS = _get_weasyprint()
            if self.css_path and os.path.exists(self.css_path):
                css = CSS(filename=self.css_path)
                HTML(string=html_content).write_pdf(output_path, stylesheets=[css])
            else:
                HTML(string=html_content).write_pdf(output_path)
        except Exception as e:
            raise Exception(f"PDF生成失败: {str(e)}")
