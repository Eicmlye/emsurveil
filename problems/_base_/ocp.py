import geatpy as ea
import numpy as np

class BaseOCP(ea.Problem):
  """
  # Args:

    - name (str): name of the problem.

    - M (int):  indicating how many targets are to be optimized. 

    - maxormins (np.ndarray): 1 indicating maximization while -1
                              indicating minimization. 

    - Dim (int): dimension of decision variable.

    - varTypes (np.ndarray):  0 indicating a continuous variable 
                              while 1 indicating a discrete one.

    - lb (np.ndarray): lower bound of decision variable.

    - ub (np.ndarray): upper bound of decision variable.

    - lbin (np.ndarray):  0 means a open half-interval at lower
                          bound while 1 means a closed one.

    - ubin (np.ndarray):  0 means a open half-interval at upper
                          bound while 1 means a closed one.
  """

  def __init__(
    self,
    name: str,
    M: int,
    maxormins: np.ndarray,
    Dim: int,
    varTypes: np.ndarray,
    lb: np.ndarray,
    ub: np.ndarray,
    lbin: np.ndarray,
    ubin: np.ndarray,
  ):
    assert maxormins.shape[0] == M
    assert varTypes.shape[0] == Dim
    assert lb.shape[0] == ub.shape[0] == Dim
    assert lbin.shape[0] == ubin.shape[0] == Dim
    super().__init__(
      name=name,
      M=M,
      maxormins=maxormins,
      Dim=Dim,
      varTypes=varTypes,
      lb=lb,
      ub=ub,
      lbin=lbin,
      ubin=ubin,
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