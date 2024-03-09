import geatpy as ea
import logging
import numpy as np

class BaseProblem(ea.Problem):
  """
  # Args:

    - is_maximize_target (np.ndarray):  1 indicating maximization while
                                        -1 indicating minimization. 

    - is_discrete_var (np.ndarray): 0 indicating a continuous variable
                                    while 1 indicating a discrete one.

    - lbound (np.ndarray): lower bound of decision variable.

    - ubound (np.ndarray): upper bound of decision variable.

    - lborder (np.ndarray): 0 means a open half-interval at lower bound
                            while 1 means a closed one.

    - uborder (np.ndarray): 0 means a open half-interval at upper bound
                            while 1 means a closed one.

    - name (str): name of the problem.
  """

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
    is_maximize_target = np.array(is_maximize_target)
    is_discrete_var = np.array(is_discrete_var)
    lbound = np.array(lbound)
    ubound = np.array(ubound)
    lborder = np.array(lborder)
    uborder = np.array(uborder)

    if is_discrete_var.ndim > 1:
      raise ValueError("is_discrete_var should be a 1D array. ")
    if is_discrete_var.shape[0] != lbound.shape[0]:
      raise ValueError(
        "The lower bounds should have the same dimension with varTypes. "
      )
    if is_discrete_var.shape[0] != ubound.shape[0]:
      raise ValueError(
        "The upper bounds should have the same dimension with varTypes. "
      )
    if lborder.shape[0] != lbound.shape[0]:
      raise ValueError(
        "The lower bound inclusion should have the same dimension with "
        "lower bounds. "
      )
    if uborder.shape[0] != ubound.shape[0]:
      raise ValueError(
        "The upper bound inclusion should have the same dimension with "
        "upper bounds. "
      )
    
    if lbound.ndim > 1:
      logging.warn("Bound and border dimensions over 1 are ignored.")

    super().__init__(
      name=name if name is not None else "Base problem",
      M=is_maximize_target.shape[0],
      maxormins=is_maximize_target,
      Dim=is_discrete_var.shape[0],
      varTypes=is_discrete_var,
      lb=lbound,
      ub=ubound,
      lbin=lborder,
      ubin=uborder,
    )

  # Rename badly formatted attributes in geatpy
  # and make them kind of read-only
  @property
  def len_target(self):
    return self.M

  @property
  def is_maximize_target(self):
    return self.maxormins

  @property
  def len_var(self):
    return self.Dim
  
  @property
  def is_discrete_var(self):
    return self.varTypes
  
  # self.ranges can be changed but it's defined according to
  # lb and ub, which is weird but we will leave this bug alone.
  # TODO: reconstruct range attribute and maybe the whole geatpy.
  @property
  def lbound(self):
    return self.lb
  
  @property
  def ubound(self):
    return self.ub
  
  @property
  def lborder(self):
    return self.borders[0]
  
  @property
  def uborder(self):
    return self.borders[1]
    

  def aimFunc(self, pop: ea.Population):
    pass
  