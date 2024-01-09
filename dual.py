import wx
import numpy as np

class LPDualPanel(wx.Panel):
    def __init__(self, parent):
        super(LPDualPanel, self).__init__(parent)

        self.optimization_type_label = wx.StaticText(self, label="Optimization Type:")
        self.optimization_type_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.variables_label = wx.StaticText(self, label="Number of Variables:")
        self.variables_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.equations_label = wx.StaticText(self, label="Number of Equations:")
        self.equations_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.obj_coef_label = wx.StaticText(self, label="Objective Coefficients:")
        self.obj_coef_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.constraints_coef_label = wx.StaticText(self, label="Constraints Coefficients:")
        self.constraints_coef_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER | wx.TE_MULTILINE)

        self.calculate_button = wx.Button(self, label="Calculate Dual")
        self.result_text = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.calculate_button.Bind(wx.EVT_BUTTON, self.on_calculate)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.optimization_type_label, 0, wx.ALL, 5)
        self.sizer.Add(self.optimization_type_text, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.variables_label, 0, wx.ALL, 5)
        self.sizer.Add(self.variables_text, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.equations_label, 0, wx.ALL, 5)
        self.sizer.Add(self.equations_text, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.obj_coef_label, 0, wx.ALL, 5)
        self.sizer.Add(self.obj_coef_text, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.constraints_coef_label, 0, wx.ALL, 5)
        self.sizer.Add(self.constraints_coef_text, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.calculate_button, 0, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.result_text, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.sizer)

    def on_calculate(self, event):
        optimization_type = self.optimization_type_text.GetValue()
        variables = int(self.variables_text.GetValue())
        equations = int(self.equations_text.GetValue())
        obj_coef = np.array([float(val) for val in self.obj_coef_text.GetValue().split()])
        constraints_coef = []

        for line in self.constraints_coef_text.GetValue().splitlines():
            temp = [float(val) for val in line.split()]
            constraints_coef.append(temp)

        result = self.dual(variables, obj_coef, equations, constraints_coef, optimization_type)
        self.result_text.SetValue(result)

    def dual(self, variables, obj_coef, equations, constrains_coef, optimization_type):
        constants = [i[-1] for i in constrains_coef]
        dual_constraints = np.transpose(constrains_coef)[:-1]
        opt = {"maximize", "minimize"} - {optimization_type}
        result_str = f"Dual of the LP problem\n{str(opt.pop()).upper()} {constants}w\nsubject to,\n"

        for i in range(len(dual_constraints)):
            left = dual_constraints[i]
            right = obj_coef[i]

            if optimization_type.lower() == 'maximize':
                result_str += f"{left}w >= {right}\n"
            else:
                result_str += f"{left}w <= {right}\n"

        result_str += "w >= 0"
        return result_str