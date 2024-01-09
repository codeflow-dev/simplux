import wx
from dual import LPDualPanel
from lpsolve import LPSolvePanel

class SimpluxFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simplux', size=(800, 600))
        self.notebook = wx.Notebook(self)

        panel1 = LPSolvePanel(self.notebook)
        self.notebook.AddPage(panel1, "Solve an LP problem")

        panel2 = LPDualPanel(self.notebook)
        self.notebook.AddPage(panel2, "Derive the dual of an LP problem")

if __name__ == '__main__':
    app = wx.App()
    frame = SimpluxFrame()
    frame.Show()
    app.MainLoop()
