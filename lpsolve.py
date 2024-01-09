import wx

class EquationPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.equation_box = wx.TextCtrl(self)
        delete_button = wx.Button(self, label="Delete")
        delete_button.Bind(wx.EVT_BUTTON, self.on_delete)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.equation_box, 1, wx.ALL, 5)
        self.sizer.Add(delete_button, 0, wx.ALL, 5)
        self.SetSizer(self.sizer)
    
    def on_delete(self, event):
        self.parent.equations.remove(self)
        event.GetEventObject().GetParent().DestroyChildren()
        self.parent.Layout()

class EquationList(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        equ = EquationPanel(self)
        self.sizer.Add(equ, 0, wx.EXPAND, 3)
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

        self.equations = [equ]

    def add_equation(self):
        equ = EquationPanel(self)
        self.sizer.Add(equ, 0, wx.EXPAND, 3)
        self.Layout()
        self.equations.append(equ)
        
class LPSolvePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, label="Objective function")
        self.sizer.Add(label, 0, wx.ALL, 10)

        objective = wx.TextCtrl(self)
        self.sizer.Add(objective, 0, wx.EXPAND | wx.ALL, 10)

        radio_box_choices = ["Maximize", "Minimize"]
        radio_box = wx.RadioBox(self, label="Choose an objective", choices=radio_box_choices, majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.sizer.Add(radio_box, 0, wx.ALL, 10)

        label2 = wx.StaticText(self, label="Constraints")
        self.sizer.Add(label2, 0, wx.ALL, 10)

        self.equ_list = EquationList(self)
        self.sizer.Add(self.equ_list, 1, wx.EXPAND, 10)

        add_button = wx.Button(self, label="Add equation")
        add_button.Bind(wx.EVT_BUTTON, self.on_add_button)
        self.sizer.Add(add_button, 0, wx.ALL, 10)

        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def on_add_button(self, event):
        self.equ_list.add_equation()

    def on_delete_button(self, event):
        event.GetEventObject().GetParent().DestroyChildren()