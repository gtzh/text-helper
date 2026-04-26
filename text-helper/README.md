# 划词助手 (Text Selection Assistant)

全局划词 AI 助手：在任意应用中选中文本，长按 Ctrl 约 0.5 秒弹出悬浮窗，提供翻译、释义、总结、改写等操作。

## 前置要求

- Python 3.10+
- AutoHotkey v2.0

## 安装和配置

### 1. 安装 Python 依赖


### 2. 配置 NewAPI

编辑 `config.yaml`，填入你的 NewAPI 服务地址和 API Key：


### 3. 运行

**方式一：手动启动**

先启动 Python 后端：


再双击 `text-helper.ahk` 启动 AHK 脚本。

**方式二：一键启动**（推荐）

直接双击 `text-helper.ahk`，脚本会自动检测并启动 Python 后端。

### 4. 开机自启（可选）

将 `text-helper.ahk` 的快捷方式放入 Windows 启动文件夹（`Win+R` → `shell:startup`）。

## 使用方法

1. 在任意应用中**选中文字**
2. **长按 Ctrl** 约 0.5 秒（不是短按，是按住不放）
3. 松开后光标旁弹出划词助手
4. 选择操作（翻译/总结/释义/改写）和模型
5. 查看 AI 回复，可追问或复制结果
6. 按 **Esc** 或点击外部关闭弹窗

## 自定义操作

编辑 `config.yaml` 的 `operations` 部分可以增加或修改操作：


## 文件结构


## 常见问题

**Q: 长按 Ctrl 没有反应？**
A: 确保 Python 后端正在运行。在命令行手动运行 `python server.py`，如果报错说明依赖未安装。

**Q: 弹窗打开但显示错误？**
A: 检查 `config.yaml` 中的 `base_url` 和 `api_key` 是否正确配置。

**Q: 如何添加更多模型？**
A: 在 `config.yaml` 的 `models` 列表中添加条目，模型 ID 必须与 NewAPI 中配置的一致。

**Q: 如何修改长按时间？**
A: 编辑 `text-helper.ahk` 中的 `holdMs := 500`，单位毫秒。
