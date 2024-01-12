import wx
from dual import LPDualPanel
from lpsolve import LPSolvePanel
from resultpanel import ResultPanel

class SimpluxFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simplux', size=(800, 800))
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.panel1 = LPSolvePanel(self)
        self.panel2 = ResultPanel(self, self.panel1)
        self.panel1.result_panel = self.panel2
        
        self.sizer.Add(self.panel1, 2, wx.ALL | wx.EXPAND, 10)
        self.sizer.Add(self.panel2, 1, wx.ALL | wx.EXPAND, 10)
        
        self.SetSizer(self.sizer)

if __name__ == '__main__':
    app = wx.App()
    frame = SimpluxFrame()
    frame.Show()
    app.MainLoop()

