import sys

import PyQt5.QtCore
import PyQt5.QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication

if len(sys.argv) > 1:

    if sys.argv[1]:

        app = QApplication(sys.argv)
        web = PyQt5.QtWebEngineWidgets.QWebEngineView()
        web.setFixedSize(815,850)
        web.load(PyQt5.QtCore.QUrl(sys.argv[1]))
        web.show()

        sys.exit(app.exec_())

# import wx 
# import wx.html2 

# class MyBrowser(wx.Dialog): 
#     def __init__(self, *args, **kwds): 
#         url = ""
#         wx.Dialog.__init__(self, *args, **kwds) 
#         sizer = wx.BoxSizer(wx.VERTICAL) 
#         self.browser = wx.html2.WebView.New(self, url=url) 
#         sizer.Add(self.browser, 1, wx.EXPAND, 10) 
#         self.SetSizer(sizer) 
#         self.SetSize((815, 850))

# if len(sys.argv) > 1:

#     if sys.argv[1]:

        # app = wx.App(useBestVisual=True) 
        # dialog = MyBrowser(None, -1) 
        # dialog.browser.LoadURL(sys.argv[1]) 
        # dialog.Show() 
        # app.MainLoop()
        # sys.exit()