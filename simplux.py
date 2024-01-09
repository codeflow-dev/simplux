import wx
from dual import LPDualPanel
from lpsolve import LPSolvePanel

class SimpluxFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Simplux', size=(800, 600))
        self.notebook = wx.Notebook(self)

        self.panel1 = LPSolvePanel(self.notebook)
        self.notebook.AddPage(self.panel1, "Solve an LP problem")

        self.panel2 = LPDualPanel(self.notebook,self.panel1)
        self.notebook.AddPage(self.panel2, "Derive the dual of an LP problem")
        
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)
    def on_page_changed(self, event):
        current_page = self.notebook.GetSelection()
        if current_page == 1:
            self.panel2.display_problem_info()

if __name__ == '__main__':
    app = wx.App()
    frame = SimpluxFrame()
    frame.Show()
    app.MainLoop()

