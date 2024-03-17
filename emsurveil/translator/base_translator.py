import geatpy as ea
import numpy as np

from emsurveil.envs import BaseOCPEnv
from emsurveil.vis.camera import BaseCameraCandidates
from emsurveil.vis.vis_mat import BaseVisMat

class BaseTranslator:
  """
  Args:
  """

  def __init__(
    self, cameras: BaseCameraCandidates, env: BaseOCPEnv, vis_mat: BaseVisMat, **kwargs
  ):
    vis_mat_shape = vis_mat.value.shape
    assert len(cameras) == env.num_voxel == vis_mat_shape[0] * vis_mat_shape[1], (
      f"Inconsistent voxel numbers among cameras ({len(cameras)}), env "
      f"({env.num_voxel}), and vis_mat ({vis_mat_shape[0] * vis_mat_shape[1]})."
    )
  

  def translate_var(self, cameras: BaseCameraCandidates, **kwargs):
    is_maximize_target = [-1]
    is_discrete_var = [0] * len(cameras)
    lbound = [0] * len(cameras)
    ubound = [1] * len(cameras)
    lborder = [1] * len(cameras)
    uborder = [1] * len(cameras)

    return is_maximize_target, is_discrete_var, lbound, ubound, lborder, uborder
  
  def translate_aim_and_constraints(
    self,
    pop: ea.Population,
    cameras: BaseCameraCandidates,
    env: BaseOCPEnv,
    vis_mat: BaseVisMat,
    **kwargs,
  ):
    var_list = []
    constraint_list = []
    for cam in range(pop.Phen.shape[1]):
      var_list.append(pop.Phen[:, [cam]])
    for tar in range(len(env.targets)):
      constraint_list.append(np.sum(vis_mat.masked_value[tar]) - 1)

    aim = np.sum(np.multiply(cameras.costs, var_list))
    constraints = np.hstack(constraint_list)

    return aim, constraints