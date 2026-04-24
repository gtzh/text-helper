# Markdown转PDF GUI工具

一个简洁的Python Tkinter GUI工具，将Markdown文件转换为GitHub风格的PDF文档。

## 功能特点

- 简洁易用的图形界面
- 支持GitHub风格PDF输出
- 实时编辑Markdown内容
- 支持代码高亮、表格、列表等完整Markdown语法
- 完善的错误提示

## 安装依赖

```bash
pip install -r requirements.txt
```

注意：Windows用户需要安装GTK/Pango依赖才能使用weasyprint。
请参考：https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
或使用MSYS2安装：`pacman -S mingw-w64-x86_64-pango`

## 运行程序

```bash
python main.py
```

或在Windows下双击 `run.bat`

## 使用方法

1. 点击"打开文件"选择Markdown文件
2. 在编辑区查看和编辑内容
3. 点击"转换为PDF"选择保存位置
4. 等待转换完成

## 技术栈

- Python 3.x
- Tkinter (GUI)
- markdown (Markdown解析)
- weasyprint (PDF生成)
- pygments (代码高亮)

## 文件结构

```
md2pdf-gui/
├── main.py              # 主程序
├── converter.py         # 转换逻辑
├── styles/
│   └── github.css      # GitHub风格样式
├── requirements.txt    # 依赖列表
└── test_samples/       # 测试样例
    └── sample.md      # 示例markdown文件
```

## 注意事项

- 确保Markdown文件使用UTF-8编码
- 首次使用需要安装依赖包
- 生成的PDF样式接近GitHub风格
- Windows上需要额外安装GTK/Pango依赖
