import logging
import numpy as np

from emsurveil.visibility import Camera, VisMat

class BaseOCPEnv:
  """
  # Args:
  """

  def __init__(
    self,
    shape: list[int],
    occupacy: list[int],
    camera: Camera,
    voxel_len: float,
    sample_step: float=0.2,
    targets: list[int]=None,
  ):
    if len(shape) != 3:
      raise ValueError(
        "`shape` should be [width, height, depth] of the space."
      )
    if not (
      len(occupacy) == len(targets) == shape[0] * shape[1] * shape[2]
      and len(occupacy) == len(camera.directions)
    ):
      raise ValueError("Inconsistent voxel numbers among inputs. ")
    if voxel_len <= 0:
      raise ValueError(f"{voxel_len} is an illegal voxel side length. ")
    if sample_step > 0.5:
      logging.warn(
        "Sampling step over 0.5 may result in mistaken vis_mat, "
        f"current sample_step == {sample_step}."
      )

    self.vis_mat = VisMat(
      shape,
      occupacy,
      camera,
      voxel_len,
      sample_step=sample_step,
      targets=targets,
    )