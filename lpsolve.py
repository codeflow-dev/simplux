import wx
import numpy as np
from equation_parser import parse_constraint, parse_objective

class EquationPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.equation_box = wx.TextCtrl(self)
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.equation_box.SetFont(font)
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

    def value(self):
        return self.equation_box.Value

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
    
    def get_equations(self):
        result = []
        for e in self.equations:
            result.append(e.value())
        return result
        
class LPSolvePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.result_panel = None

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        
        label = wx.StaticText(self, label="Objective function")
        self.sizer.Add(label, 0, wx.ALL, 10)

        self.objective = wx.TextCtrl(self)
        self.objective.SetFont(font)
        self.sizer.Add(self.objective, 0, wx.EXPAND | wx.ALL, 10)

        label2 = wx.StaticText(self, label="Number of decision variables")
        self.sizer.Add(label2, 0, wx.ALL, 10)

        self.n = wx.TextCtrl(self)
        self.n.SetFont(font)
        self.sizer.Add(self.n, 0, wx.EXPAND | wx.ALL, 10)

        radio_box_choices = ["Maximize", "Minimize"]
        self.radio_box = wx.RadioBox(self, label="Choose an objective", choices=radio_box_choices, majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.sizer.Add(self.radio_box, 0, wx.ALL, 10)

        label2 = wx.StaticText(self, label="Constraints")
        self.sizer.Add(label2, 0, wx.ALL, 10)

        self.equ_list = EquationList(self)
        self.sizer.Add(self.equ_list, 1, wx.ALL | wx.EXPAND, 10)

        add_button = wx.Button(self, label="Add equation")
        add_button.Bind(wx.EVT_BUTTON, self.on_add_button)
        self.sizer.Add(add_button, 0, wx.ALL, 10)

        solve_button = wx.Button(self, label="Solve problem")
        solve_button.Bind(wx.EVT_BUTTON, self.on_solve_button)
        self.sizer.Add(solve_button, 0, wx.ALL, 10)


        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def on_add_button(self, event):
        self.equ_list.add_equation()

    def on_solve_button(self, event):
        obj = self.objective.Value
        constraints = self.equ_list.get_equations()
        n = int(self.n.Value)
        minimize = bool(self.radio_box.Selection)
        result, r = simplex(obj, constraints, n, minimize)
        self.result_panel.set_result1(result)
        self.result_panel.dual_panel.display_problem_info()
        self.result_panel.set_image(constraints, n, r)

    def on_delete_button(self, event):
        event.GetEventObject().GetParent().DestroyChildren()

    def get_objective_info(self):
        objective_type = self.radio_box.GetStringSelection()
        objective_function = self.objective.GetValue()
        constraints = [equ.equation_box.GetValue() for equ in self.equ_list.equations]

        return objective_type, objective_function, constraints

# constraints = ["4x1-6x2-5x3-4x4>=-20", "-3x1-2x2+4x3+x4<=10", "-8x1-3x2+3x3+2x4<=20"]
# obj = "-4x1-x2-3x3-5x4"
# n = 4
# constraints = ["x1+2x2+x3<=430", "3x1+2x3<=460", "x1+4x2<=420"]
# obj = "3x1+2x2+5x3+9"
# n = 3
# constraints = ["5x1+4x2<=32", "x1+2x2<=10"]
# obj = "-2x1-3x2-9"
# n = 2
def simplex(obj, constraints, n, minimize):
    obj_coeff, obj_const = parse_objective(obj, n)
    obj_coeff = np.array(obj_coeff)
    obj_coeff = np.concatenate((obj_coeff * -1, np.zeros(len(constraints)), [obj_const]))
    if minimize:
        obj_coeff *= -1
    # print("Objective:", obj_coeff)
    constraints = [parse_constraint(i, n) for i in constraints]
    # print("Constraints:", constraints)
    mat = np.array([i[0] for i in constraints])
    constraints_const = np.array([i[2] for i in constraints])
    constraints_const = np.reshape(constraints_const, (-1, 1))
    for i in range(len(constraints)):
        if constraints[i][1] == ">=":
            mat[i] *= -1
            constraints_const[i] *= -1
    mat = np.concatenate((mat, np.identity(len(constraints)), constraints_const), axis=1)

    head = ["x" + str(i+1) for i in range(n)] + ["s" + str(i+1) for i in range(len(constraints))]
    left = ["s" + str(i+1) for i in range(len(constraints))]
    print(obj_coeff)
    print(mat)

    key_column = np.argmin(obj_coeff[:-1])
    while obj_coeff[key_column] < 0:
        ratio = mat[:, -1] / mat[:, key_column]
        print(ratio)
        ratio = np.where(ratio > 0, ratio, np.inf)
        key_row = np.argmin(ratio)
        if ratio[key_row] == np.inf:
            return "No solution available"
        
        # Divide whole row by key item
        mat[key_row] /= mat[key_row][key_column]

        # Subtract from other rows
        for i in range(mat.shape[0]):
            if i != key_row:
                mat[i] -= mat[i][key_column] * mat[key_row]
        
        # Subtract from obj row
        obj_coeff -= obj_coeff[key_column] * mat[key_row]

        left[key_row] = head[key_column]
        # print(head)
        # print(obj_coeff)
        # print(mat)
        # print(left)
        key_column = np.argmin(obj_coeff[:-1])

    result = f"Z{'min' if minimize else 'max'} = {-obj_coeff[-1] if minimize else obj_coeff[-1]}\n"
    r = [0] * n
    for i in range(len(left)):
        if left[i][0] == 'x':
            r[int(left[i][1])-1] = mat[i][-1]
    for i in range(len(r)):
        result += f"x{i+1} = {r[i]}\n"
    return result, r

# print(simplex(obj, constraints, n, False))