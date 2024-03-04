import geatpy as ea
import numpy as np

class BaseOCP(ea.Problem):
  """
  # Args:

    - name (str): name of the problem.

    - M (int): dimension of target, indicating how many targets are to be optimized. 

    - maxormins (np.ndarray): 1 indicating maximization while -1 indicating minimization. 

    - Dim (int): dimension of decision variable.

    - varTypes (np.ndarray):  0 indicating a continuous variable 
                              while 1 indicating a discrete one.

    - lb (np.ndarray): lower bound of decision variable.

    - ub (np.ndarray): upper bound of decision variable.

    - lbin (np.ndarray): 0 means a open half-interval at lower bound while 1 means a closed one.

    - ubin (np.ndarray): 0 means a open half-interval at upper bound while 1 means a closed one.
  """

  def __init__(
    self,
    name: str="Base OCP Problem. ",
    M: int=None,
    maxormins: np.ndarray=[],
    Dim: int=None,
    varTypes: np.ndarray=[],
    lb: np.ndarray=[],
    ub: np.ndarray=[],
    lbin: np.ndarray=[],
    ubin: np.ndarray=[],
  ):
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
    pass