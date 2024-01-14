import wx
from dual import LPDualPanel
from equation_parser import parse_constraint
from problemplot import plot_problem

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
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.textbox1.SetFont(font)
        self.dual_panel = LPDualPanel(self.tab2, lp_solve_panel)
        self.plot_panel = wx.StaticBitmap(self.tab3, wx.ID_ANY)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.textbox1, 1, wx.EXPAND, 10)
        self.tab1.SetSizer(sizer1)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.dual_panel, 1, wx.EXPAND, 10)
        self.tab2.SetSizer(sizer2)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(self.plot_panel, 1, wx.EXPAND, 10)
        self.tab3.SetSizer(sizer3)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.notebook, 1, wx.EXPAND)

        self.SetSizer(main_sizer)

    def set_result1(self, text):
        self.textbox1.Value = text

    def set_image(self, constraints, n, r):
        if n <= 2:
            constraints = [parse_constraint(i, n) for i in constraints]
            cos = [i[0] for i in constraints]
            constants = [i[2] for i in constraints]
            plot_problem(cos, constants, r)
            image_path = "output.png"  # Replace with the path to your image file
            image = wx.Image(image_path, wx.BITMAP_TYPE_ANY)
            self.plot_panel.Bitmap = wx.Bitmap(image)
