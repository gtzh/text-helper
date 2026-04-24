import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
from converter import MarkdownConverter

class MarkdownToPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown转PDF工具")
        self.root.geometry("800x600")
        
        self.converter = MarkdownConverter()
        self.current_file = None
        
        self._create_menu()
        self._create_toolbar()
        self._create_text_area()
        self._create_status_bar()
    
    def _create_menu(self):
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="打开", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def _create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        btn_open = tk.Button(toolbar, text="打开文件", command=self.open_file)
        btn_open.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_convert = tk.Button(toolbar, text="转换为PDF", command=self.convert_to_pdf)
        btn_convert.pack(side=tk.LEFT, padx=2, pady=2)
        
        btn_about = tk.Button(toolbar, text="关于", command=self.show_about)
        btn_about.pack(side=tk.LEFT, padx=2, pady=2)
    
    def _create_text_area(self):
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 11))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="就绪", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="选择Markdown文件",
            filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                
                self.current_file = file_path
                self.status_bar.config(text=f"已加载: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("错误", f"无法读取文件: {str(e)}")
    
    def convert_to_pdf(self):
        if not self.current_file:
            messagebox.showwarning("警告", "请先打开一个Markdown文件")
            return
        
        # 获取保存路径
        output_path = filedialog.asksaveasfilename(
            title="保存PDF",
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf")],
            initialfile=os.path.splitext(os.path.basename(self.current_file))[0] + ".pdf"
        )
        
        if not output_path:
            return
        
        # 更新状态
        self.status_bar.config(text="正在转换...")
        self.root.update()
        
        # 执行转换
        success, message = self.converter.convert_file(self.current_file, output_path)
        
        if success:
            messagebox.showinfo("成功", message)
            self.status_bar.config(text=message)
        else:
            messagebox.showerror("转换失败", message)
            self.status_bar.config(text="转换失败")
    
    def show_about(self):
        messagebox.showinfo("关于", "Markdown转PDF工具\n版本 1.0\n\n使用Python + Tkinter开发\n支持GitHub风格PDF输出")

def main():
    root = tk.Tk()
    app = MarkdownToPDFApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
