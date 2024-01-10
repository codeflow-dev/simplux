import re

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
                if m.group(1) == '+':
                    co[i-1] += 1
                elif m.group(1) == '-':
                    co[i-1] -= 1
                else:
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
