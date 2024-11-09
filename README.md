# 微信回复建议助理

## 介绍

- 实时读取微信聊天记录。
- 调用 OpenAI API 生成回复建议，以便用户参考。
- 支持微信多开。

## 使用方法

### 启动

支持微信版本：3.9+

[微信各版本下载](https://github.com/tom-snow/wechat-windows-versions/releases)

先登录微信。保持微信在桌面。

不要点右上角的关闭。最小化没问题。

点击 exe 程序启动即可。

### 关闭

关闭终端或者关闭助手窗口

## 开发

### 环境

Python 3.11

### 代码

代码主入口 `main.py`

项目在[wxauto](https://github.com/cluic/wxauto)基础上进行了增强。

- 支持微信多开
- 新增方法`InputMsg`，输入信息，不会马上发送，使用方式与`SendMsg`相同。

### 打包

使用[pyinstaller](https://github.com/pyinstaller/pyinstaller)打包生成 exe

```bash
pyinstaller --onefile main.py --name "微信回复建议助理"
```

常用选项

- onefile：将所有内容打包成一个单独的可执行文件。
- windowed：如果你的应用程序是一个 GUI 应用程序，不希望出现控制台窗口，可以使用这个选项（适用于 Windows 和 macOS）。
- name：指定生成的可执行文件的名称。
- icon：指定图标文件（.ico 或 .icns）。
- add-data：添加额外的数据文件或目录。

## 开发辅助工具

可以使用 [installer](https://github.com/yinkaisheng/Python-UIAutomation-for-Windows/tree/master/inspect) 来定位查看控件信息。

## 开发原理

1. 借助 Python 库[wxauto](https://github.com/cluic/wxauto)查看 GUI 控件信息，获取聊天历史记录。
2. 使用 Python 内置库`tkinter`创建跟随窗口。
3. 启动事件`tkinter`循环，不断监听聊天记录及窗口位置。
4. 聊天记录得到更新后，传递给`openai`，拿到回复，将回复推到跟随窗口中。

## 感谢

感谢[wxauto](https://github.com/cluic/wxauto)作者的开源，让微信自动化有更多可能，可以实现聊天机器人、群发等功能。
