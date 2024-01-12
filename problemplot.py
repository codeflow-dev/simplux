from ctypes import sizeof
import matplotlib.pyplot as plt
import numpy as np


def plot_problem(cos, constants, max_point):
  n = len(constants)
  val = 0.0
  for i in range(n):
    for j in range(2):
      val = max(val, constants[i]/cos[i][j])

  x = np.arange(0, val+1)

  for co, constant in zip(cos, constants):
    m=-(co[0]/co[1])
    c=constant/co[1]
    plt.plot(x, m*x+c, color='red', linestyle='solid')

  plt.xlim(0.0, val)
  plt.ylim(0, val)
  plt.axhline(0, color='black',linewidth=1.5)
  plt.axvline(0, color='black',linewidth=1.5)

  if(constants[0]/cos[0][0] > constants[1]/cos[1][0]):
    equation = f'y = {-cos[0][0]}/{cos[0][1]} * x + {constants[0]}/{cos[0][1]}'
    x_pos = constants[0]/cos[0][0] - (constants[0]/cos[0][0])*0.1  # Adjust this value to change the position of the text along x-axis
    y_pos = (constants[0]/cos[0][0])*0.1  # Calculate y-position based on the equation
    plt.text(x_pos, y_pos, equation, fontsize=10, color='blue')

    equation = f'y = {-cos[1][0]}/{cos[1][1]} * x + {constants[1]}/{cos[1][1]}'
    x_pos = (constants[1]/cos[1][1])*0.1  # Adjust this value to change the position of the text along x-axis
    y_pos = (constants[1]/cos[1][1]) - (constants[1]/cos[1][1])*0.1  # Calculate y-position based on the equation
    plt.text(x_pos, y_pos, equation, fontsize=10, color='blue')

  plt.grid()
  plt.savefig("output.png")