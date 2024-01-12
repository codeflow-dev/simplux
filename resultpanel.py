import wx
from dual import LPDualPanel

class ResultPanel(wx.Panel):
    def __init__(self, parent, lp_solve_panel):
        super(ResultPanel, self).__init__(parent)

        self.notebook = wx.Notebook(self)

        self.tab1 = wx.Panel(self.notebook)
        self.tab2 = wx.Panel(self.notebook)
        self.tab3 = wx.Panel(self.notebook)

        self.notebook.AddPage(self.tab1, "Solution")
        self.notebook.AddPage(self.tab2, "Dual")
        self.notebook.AddPage(self.tab3, "Visualization")

        self.textbox1 = wx.TextCtrl(self.tab1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.dual_panel = LPDualPanel(self.tab2, lp_solve_panel)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.textbox1, 1, wx.EXPAND, 10)
        self.tab1.SetSizer(sizer1)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.dual_panel, 1, wx.EXPAND, 10)
        self.tab2.SetSizer(sizer2)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.notebook, 1, wx.EXPAND)

        self.SetSizer(main_sizer)

    def set_result1(self, text):
        self.textbox1.Value = text
