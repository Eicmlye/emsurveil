import numpy as np

from emsurveil.envs._base_ import BaseOCPEnv


class BaseFullyCoverEnv(BaseOCPEnv):
  """
  # Args:
  """

  def __init__(
    self,
    cam_candidates: list[int],
    targets: list[int],
    costs: list[int],
    visibility: np.ndarray,
  ):
    costs = np.array(costs)

    if costs.ndim > 1:
      raise ValueError("costs should be a 1D array. ")
    if costs.shape[0] != cam_candidates.shape[0]:
      raise ValueError(
        "Got different numbers of voxel in cam_candidates "
        f"({cam_candidates.shape[0]}) and costs "
        f"({costs.shape[0]}). "
      )

    self.costs = costs
    self.vis = visibility
    super().__init__(
      cam_candidates,
      targets,
    )