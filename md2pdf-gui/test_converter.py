# test_converter.py
from converter import MarkdownConverter
import os

def test_markdown_to_html():
    """测试markdown转HTML功能"""
    print("=" * 50)
    print("Test 1: Markdown to HTML")
    print("=" * 50)
    
    converter = MarkdownConverter()
    test_md = """# Title
    
## Subtitle

This is **bold** and *italic* text.

```python
def hello():
    print("Hello")
```

- Item 1
- Item 2
"""
    
    try:
        html = converter._markdown_to_html(test_md)
        # 检查是否包含预期的HTML元素（允许有属性）
        if "<h1" in html and "<strong>" in html and "<code>" in html:
            print("[PASS] Markdown to HTML successful")
            print(f"  HTML length: {len(html)} characters")
            return True
        else:
            print("[FAIL] HTML content incomplete")
            print(f"  Debug: h1 present: {'<h1' in html}, strong present: {'<strong>' in html}, code present: {'<code>' in html}")
            return False
    except Exception as e:
        print(f"[FAIL] Markdown to HTML failed: {e}")
        return False

def test_convert_file():
    """测试完整转换功能"""
    print("\n" + "=" * 50)
    print("Test 2: Full Conversion (Markdown to PDF)")
    print("=" * 50)
    
    converter = MarkdownConverter()
    
    input_file = "test_samples/sample.md"
    output_file = "test_samples/output.pdf"
    
    if not os.path.exists(input_file):
        print(f"[FAIL] Test file not found: {input_file}")
        return False
    
    print(f"Converting: {input_file}")
    try:
        success, message = converter.convert_file(input_file, output_file)
        
        if success:
            print(f"[PASS] {message}")
            print(f"  Output file: {output_file}")
            print(f"  File size: {os.path.getsize(output_file)} bytes")
            return True
        else:
            print(f"[FAIL] {message}")
            if "libgobject" in message or "cannot load library" in message or "WeasyPrint" in message:
                print("\nNote: GTK/Pango dependencies required on Windows")
                print("Solutions:")
                print("1. Install MSYS2: https://www.msys2.org/")
                print("2. In MSYS2, run: pacman -S mingw-w64-x86_64-pango")
                print("3. Set env var: set WEASYPRINT_DLL_DIRECTORIES=C:\\msys64\\mingw64\\bin")
                print("Or use WSL")
            return False
    except Exception as e:
        print(f"[FAIL] Conversion exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 50)
    print("Test 3: Error Handling")
    print("=" * 50)
    
    converter = MarkdownConverter()
    
    # 测试文件不存在
    success, msg = converter.convert_file("nonexistent.md", "out.pdf")
    if not success and "not found" in msg.lower() or "不存在" in msg:
        print("[PASS] Correctly handled non-existent file")
    else:
        print(f"[FAIL] Non-existent file handling error: {msg}")
        return False
    
    # 测试非md文件
    success, msg = converter.convert_file("test_converter.py", "out.pdf")
    if not success and "markdown" in msg.lower() or "markdown文件" in msg:
        print("[PASS] Correctly handled non-markdown file")
    else:
        print(f"[FAIL] Non-markdown file handling error: {msg}")
        return False
    
    return True

if __name__ == "__main__":
    print("\nMarkdown to PDF Converter Tests\n")
    
    results = []
    results.append(("Markdown to HTML", test_markdown_to_html()))
    
    try:
        results.append(("Full Conversion", test_convert_file()))
    except Exception as e:
        print(f"Full conversion test exception: {e}")
        results.append(("Full Conversion", False))
    
    results.append(("Error Handling", test_error_handling()))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{name}: {status}")
