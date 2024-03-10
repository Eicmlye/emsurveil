import numpy as np


class BaseOCPEnv:
  """
  # Args:
  """

  def __init__(
    self,
    cam_candidates: list[int],
    targets: list[int],
  ):
    cam_candidates = np.array(cam_candidates)
    targets = np.array(targets)

    if cam_candidates.ndim > 1:
      raise ValueError("cam_candidates should be a 1D array. ")
    if targets.ndim > 1:
      raise ValueError("targets should be a 1D array. ")
    if cam_candidates.shape[0] != targets.shape[0]:
      raise ValueError(
        "Got different numbers of voxel in cam_candidates "
        f"({cam_candidates.shape[0]}) and targets "
        f"({targets.shape[0]}). "
      )

    self.cam_candidates = cam_candidates
    self.targets = targets