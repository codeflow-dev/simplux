import wx
import numpy as np
from equation_parser import parse_objective, parse_constraint

class LPDualPanel(wx.Panel):
    def __init__(self, parent, lp_solve_panel):
        super(LPDualPanel, self).__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.lp_solve_panel = lp_solve_panel
        self.problem_label = wx.StaticText(self, label="")
        self.dual_label = wx.StaticText(self, label="")
        self.sizer.Add(self.problem_label, 0, wx.ALL, 10)
        self.sizer.Add(self.dual_label, 0, wx.ALL | wx.EXPAND, 10)
        self.SetSizer(self.sizer)
        self.display_problem_info()

    def display_problem_info(self):
        try:
            objective_type, objective_function, constraints = self.lp_solve_panel.get_objective_info()
            font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.problem_label.SetFont(font)
            self.dual_label.SetFont(font)
            print(objective_function)
            n = 0
            for i in range(len(objective_function)):
                if objective_function[i] == 'x' and objective_function[i+1].isdigit():
                    n = max(n, int(objective_function[i+1]))

            obj_coef, constant = parse_objective(str(objective_function), n)
            #print("n:", n)
            # Parse each constraint
            constrains_coef = []
            for constraint in constraints:
                cons_coef, sign, constant = parse_constraint(str(constraint), n)
                cons_coef.append(constant)
                constrains_coef.append(cons_coef)
            
            font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.problem_label.SetFont(font)
            self.dual_label.SetFont(font)
            if (objective_type=='Maximize' and sign=='>=') or (objective_type=='Minimize' and sign=='<='):
                self.problem_label.setLabel("you have made an error!")
                self.dual_label.SetLabel("No dual")
                raise Exception("Contradictory problem details. Please correct it")

            else:
                # Display the problem in the panel
                problem_text = f"Your given problem:\n{objective_type} {objective_function}\nSubject to,\n" 
                for constraint in constraints:
                    problem_text+=constraint+"\n"
                for i in range(0,n):
                    if i+1<n:
                        problem_text+=f"x{i+1},"
                    else:
                        problem_text+=f"x{i+1}>=0"
                self.problem_label.SetLabel(problem_text)

                # Display the dual in the panel
                dual_result = self.dual(n, obj_coef, constraints, constrains_coef, objective_type)
                self.dual_label.SetLabel(dual_result)

                self.Layout()

        except Exception as e:
            print(f"Error: {e}")
            print(f"Objective Type: {objective_type}")
            print(f"Objective Function: {str(objective_function)}")
            print(f"Constraints: {constraints}")

    def dual(self, variables, obj_coef, equations, constrains_coef, objective_type):
        constants = [i[-1] for i in constrains_coef]
        dual_constraints = np.transpose(constrains_coef)[:-1]
        opt = {"Maximize", "Minimize"} - {objective_type}
        result_str = f"Dual of the LP problem\n{str(opt.pop())} "
        result_str += ','
        for i in range(len(list(constants))):
            if i > 0 and int(constants[i]) > -1:
                result_str += '+'
            result_str += str(constants[i]) + "w" + str(f"{i + 1}")
        result_str += "\nsubject to,\n"
        for i in range(len(dual_constraints)):
            result_str +="\t"
            left = list(dual_constraints[i])
            right = obj_coef[i]
            for i in range(len(left)):
                if i > 0 and int(left[i]) > -1:
                    result_str += '+'
                result_str += str(left[i]) + "w" + str(f"{i + 1}")
            if objective_type== 'Maximize':
                result_str += " >= "
            else:
                result_str += " <= "
            result_str += str(right) + "\n"

        result_str += "\twi >= 0"
        return result_str


