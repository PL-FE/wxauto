import time
from wxauto_custom import *
import uiautomation as uia
import threading
import tkinter as tk
import assistant
import json
import win32gui

window_title = 'AI回复助理'


def check_window_visibility(window, wx):
    # 获取微信窗口句柄和位置
    wechat_hwnd = wx.UiaAPI.NativeWindowHandle
    if wechat_hwnd:
        # 获取当前鼠标点击的窗口的句柄的标题
        current_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())

        # 判断微信窗口状态，显示或隐藏本窗口
        if win32gui.GetForegroundWindow() == wechat_hwnd or current_title == window_title:
            window.wm_attributes('-alpha', 1.0)
        else:
            window.wm_attributes('-alpha', 0.0)
    else:
        # 微信窗口未找到，隐藏本窗口
        window.wm_attributes('-alpha', 0.0)


class WxAutoAssistant:
    def __init__(self):
        self.wechats = self.find_wechat_windows()
        self.gpt_assistant = assistant.ChatGPTClient()

    def find_wechat_windows(self):
        root = uia.GetRootControl()
        child = root.GetChildren()
        filtered_list = list(filter(lambda x: x.ClassName == 'WeChatMainWndForPC', child))
        return [WeChat(wx_window) for wx_window in filtered_list]

    def create_assistant_window(self):
        window = tk.Tk()
        window.title(window_title)
        window.overrideredirect(True)
        window.wm_attributes('-topmost', True)
        self.create_title_bar(window)
        self.create_close_button(window)
        return window

    def create_title_bar(self, window):
        title_frame = tk.Frame(window, height=30)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text=window.title())
        title_label.pack(side=tk.LEFT, padx=5)
        window.title_frame = title_frame
        window.title_label = title_label

    def create_close_button(self, window):
        close_button = tk.Button(window.title_frame, text="X", command=window.destroy, height=1)
        close_button.pack(side=tk.RIGHT, padx=5)
        window.close_button = close_button

    def handle_wechat_window(self, wx):
        chats_list = []
        labels = []
        try:
            assistant_window = self.create_assistant_window()
            self.update_window_position(assistant_window, wx)  # 开始时刻跟随微信窗口
            self.update_chat_messages(assistant_window, wx, chats_list, labels)  # 更新聊天内容
            assistant_window.mainloop()
        except Exception as e:
            print(f"处理微信窗口失败: {e}")

    def update_chat_messages(self, window, wx, chats_list, labels):
        msgs = wx.GetAllMessage()
        msgs.reverse()
        chats_list_temp = []

        for msg in msgs:
            if msg.type == 'friend':
                chats_list_temp.append({'nickname': msg.sender_remark, 'content': msg.content, 'is_send': False})
            elif msg.type == 'self':
                chats_list_temp.append({'nickname': '', 'content': msg.content, 'is_send': True})

        if chats_list_temp != chats_list:
            res_msg = self.gpt_assistant.get_response(chats_list_temp)
            self.display_chat_tips(window, wx, res_msg, labels)
            chats_list = chats_list_temp
            print('新消息:', chats_list_temp)

        window.after(3000, self.update_chat_messages, window, wx, chats_list, labels)

    def display_chat_tips(self, window, wx, res_msg, labels):
        for label in labels:
            label.destroy()
        labels.clear()

        for msg in json.loads(res_msg):
            label = tk.Label(window, text=msg, wraplength=200, justify=tk.LEFT)
            label.pack()
            label.bind("<Button-1>", lambda event, m=msg: wx.InputMsg(m))
            labels.append(label)

    def update_window_position(self, window, wx):
        try:
            check_window_visibility(window, wx)

            rect = wx.UiaAPI.BoundingRectangle
            wx_width = rect.width()
            wx_height = rect.height()
            wx_x = rect.left
            wx_y = rect.top
            window.geometry(f'200x{wx_height}+{wx_x + wx_width}+{wx_y}')
            window.after(100, self.update_window_position, window, wx)
        except IndexError:
            print("未找到微信窗口，请确保微信已启动")


# 主程序
if __name__ == "__main__":
    wxAutoAssistant = WxAutoAssistant()
    threads = []

    for wx in wxAutoAssistant.wechats:
        thread = threading.Thread(target=wxAutoAssistant.handle_wechat_window, args=(wx,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
