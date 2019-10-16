import sys
import wx


class MyFrame(wx.Frame):
    # 用户登录成功后,保存当前用户信息
    Session = {}

    def __init__(self, title, size):
        super().__init__(parent=None, title=title, size=size, style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)
        # 设置窗口居中
        self.Center()
        # 设置Frame窗口内容面板
        self.contentpanel = wx.Panel(parent=self)
        ico = wx.Icon('resources/icon/dog4.ico', wx.BITMAP_TYPE_ICO)
        # 设置窗口图标
        self.SetIcon(ico)
        # 设置窗口的最大和最小尺度
        self.SetSizeHints(size, size)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        # 退出系统
        self.Destroy()
        sys.exit()
