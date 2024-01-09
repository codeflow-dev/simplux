import re
import numpy as np

def terms(expression):
    expression = expression.replace(" ", "")
    term_list = []
    current_term = ''
    for char in expression:
        if char in ['+', '-']:
            if current_term:
                term_list.append(current_term)
            current_term = char
        else:
            current_term += char
    if current_term:
        term_list.append(current_term)
    return term_list

def parse_objective(expression, n):
    term_list = terms(expression)
    co = [0] * n
    constant = 0
    for term in term_list:
        m = re.search(r'([+-]?\d*)x(\d+)', term)
        if m:
            i = int(m.group(2))
            if m.group(1):
                co[i-1] += int(m.group(1))
            else:
                co[i-1] += 1
        else:
            constant += int(term)
    return co, constant

def parse_constraint(equation, n):
    match = re.match(r'(.+)<=(.+)', equation)
    if match:
        left_side = match.group(1).strip()
        right_side = match.group(2).strip()
        sign = '<='
    else:
        match = re.match(r'(.+)>=(.+)', equation)
        if match:
            left_side = match.group(1).strip()
            right_side = match.group(2).strip()
            sign = '>='
        else:
            raise Exception(f"Invalid constraint {equation}")
    left_side = terms(left_side)
    right_side = terms(right_side)
    co = [0] * n
    constant = 0
    for term in left_side:
        m = re.search(r'([+-]?\d*)x(\d+)', term)
        if m:
            i = int(m.group(2))
            if m.group(1):
                if m.group(1) == '+':
                    co[i-1] += 1
                elif m.group(1) == '-':
                    co[i-1] -= 1
                else:
                    co[i-1] += int(m.group(1))
            else:
                co[i-1] += 1
        else:
            constant -= int(term)
    for term in right_side:
        m = re.search(r'([+-]?\d*)x(\d+)', term)
        if m:
            i = int(m.group(2))
            if m.group(1):
                if m.group(1) == '+':
                    co[i-1] -= 1
                elif m.group(1) == '-':
                    co[i-1] += 1
                else:
                    co[i-1] -= int(m.group(1))
            else:
                co[i-1] -= 1
        else:
            constant += int(term)
    return co, sign, constant

# constraints = ["2x1+x2<=3", "3x1+5x2<=9", "x1+3x2<=5"]
# obj = "x1+4x2"
# n = 2
# constraints = ["x1+2x2+x3<=430", "3x1+2x3<=460", "x1+4x2<=420"]
# obj = "3x1+2x2+5x3"
# n = 3
def simplex(obj, constraints, n):
    obj_coeff, obj_const = parse_objective(obj, n)
    obj_coeff = np.array(obj_coeff)
    obj_coeff = np.concatenate((obj_coeff * -1, np.zeros(len(constraints)), [obj_const]))
    # print("Objective:", obj_coeff)
    constraints = [parse_constraint(i, n) for i in constraints]
    # print("Constraints:", constraints)
    mat = [i[0] for i in constraints]
    constraints_const = np.array([i[2] for i in constraints])
    constraints_const = np.reshape(constraints_const, (-1, 1))
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
            raise ValueError("No smallest positive ratio found")
        
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

    result = f"Zmax = {obj_coeff[-1]}\n"
    for i in range(len(left)):
        if left[i][0] == 'x':
            result += f"{left[i]} = {mat[i][-1]}"
    return result