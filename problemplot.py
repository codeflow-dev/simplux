from ctypes import sizeof
import matplotlib.pyplot as plt
import numpy as np


def plot_problem(cos, constants, r):
  n = len(constants)
  val = 0.0
  for i in range(n):
    for j in range(2):
      val = max(val, constants[i]/cos[i][j])

  x = np.arange(0, val+1)

  plt.figure("Constraints")

  for co, constant in zip(cos, constants):
    m=-(co[0]/co[1])
    c=constant/co[1]
    plt.plot(x, m*x+c, color='red', linestyle='solid')

  plt.plot([r[0]], [r[1]], marker="o", markersize=5, markerfacecolor="black")
  plt.text(r[0]*1.02, r[1]*1.02, f"Optimized point = ({round(r[0], 2)}, {round(r[1], 2)})", fontsize=10, color='black')
  plt.xlim(0.0, val)
  plt.ylim(0, val)
  plt.axhline(0, color='black',linewidth=1.5)
  plt.axvline(0, color='black',linewidth=1.5)
  plt.xlabel("x1")
  plt.ylabel("x2")

  plt.grid()
  plt.savefig("output.png")
  plt.cla()
# plot_problem([[4, 3], [3, 4]], [12, 12], [1.7142857142857144, 1.7142857142857144])