import geatpy as ea
import numpy as np

from emsurveil.problems._base_ import BaseOCPProblem

class ExampleProblem(BaseOCPProblem):
  def __init__(
    self,
    is_maximize_target: list[int],
    is_discrete_var: list[int],
    lbound: list[int],
    ubound: list[int],
    lborder: list[int],
    uborder: list[int],
    name: str=None,
  ):
    super().__init__(
      is_maximize_target,
      is_discrete_var,
      lbound,
      ubound,
      lborder,
      uborder,
      name,
    )
    
  def aimFunc(self, pop: ea.Population):
    Vars = pop.Phen
    x1 = Vars[:, [0]]
    x2 = Vars[:, [1]]
    x3 = Vars[:, [2]]

    pop.ObjV = 4 * x1 + 2 * x2 + x3

    pop.CV = np.hstack([
      2 * x1 + x2 - 1,
      x1 + 2 * x3 - 2,
      np.abs(x1 + x2 + x3 - 1),
    ])

