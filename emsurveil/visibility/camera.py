import math
import numpy as np
from tqdm import tqdm


class Camera:
  """
  # Args:

    - directions (list[list[float]]): the [span, tilt] direction of
        cameras in radians.

    - clip_shape (list[list[float]]): the [width, height] of clips in
        meters.

    - focal_len (list[list[float]]): the focal length of cameras in
        meters.

    - resolution (list[list[float]]): [width, height] resolutions of
        images shot by cameras in pixels.

    - horizontal_resol (list[list[float]]): [min, max] of the horizontal
        resolution requirements for cameras in pixels per meter.

    - vertical_resol (list[list[float]]): [min, max] of the vertical
        resolution requirements for cameras in pixels per meter.

  # Attributes:

    - directions (list[list[float]]): the [span, tilt] direction of
        cameras in radians.

    - dof (list[list[float]]): the [near, far] DoFs of cameras in
        meters.

    - horizontal_angles (list[float]): the horizontal FoV angles of
        cameras in radians.

    - vertical_angles (list[float]): the vertical FoV angles of cameras
        in radians.
  """

  def __init__(
    self,
    directions: list[list[float]],
    clip_shape: list[list[float]],
    focal_len: list[float],
    resolution: list[list[float]],
    horizontal_resol: list[list[float]],
    vertical_resol: list[list[float]],
  ):
    if not (
      len(directions) == len(clip_shape) == len(focal_len)
      and len(clip_shape) == len(resolution) == len(horizontal_resol)
      and len(clip_shape) == len(vertical_resol)
    ):
      raise ValueError("Inconsistent voxel numbers among inputs. ")
    self.__directions = directions
    self.__dof = self._compute_dof(
      clip_shape,
      focal_len,
      resolution,
      horizontal_resol,
      vertical_resol,
    )
    self.__horizontal_angles = [
      2 * math.atan(clip_shape[cam][0] / focal_len[cam] / 2)
      for cam in range(len(clip_shape))
    ]
    self.__vertical_angles = [
      2 * math.atan(clip_shape[cam][1] / focal_len[cam] / 2)
      for cam in range(len(clip_shape))
    ]


  @property
  def directions(self):
    return self.__directions

  @property
  def dof(self):
    return self.__dof

  @property
  def horizontal_angles(self):
    return self.__horizontal_angles

  @property
  def vertical_angles(self):
    return self.__vertical_angles

  def _compute_dof(
    self,
    clip_shape: list[list[float]],
    focal_len: list[float],
    resolution: list[list[float]],
    horizontal_resol: list[list[float]],
    vertical_resol: list[list[float]],
  ):
    """
    # Args:

      - clip_shape (list[list[float]]): the [width, height] of clips in
          meters.

      - focal_len (list[list[float]]): the focal length of cameras in
          meters.

      - resolution (list[list[float]]): [width, height] resolutions of
          images shot by cameras

      - horizontal_resol (list[list[float]]): [min, max] of the horizontal
          resolution requirements for cameras

      - vertical_resol (list[list[float]]): [min, max] of the vertical
          resolution requirements for cameras
    """
    dof = []
    for cam in range(len(clip_shape)):
      cam_dof = []
      # near limit of DoF
      width_near = resolution[cam][0] / horizontal_resol[cam][1]
      height_near = resolution[cam][1] / vertical_resol[cam][1]
      cam_dof.append(max(
        focal_len[cam] * width_near / clip_shape[cam][0],
        focal_len[cam] * height_near / clip_shape[cam][1],
      ))
      # far limit of DoF
      width_far = resolution[cam][0] / horizontal_resol[cam][0]
      height_far = resolution[cam][1] / vertical_resol[cam][0]
      cam_dof.append(min(
        focal_len[cam] * width_far / clip_shape[cam][0],
        focal_len[cam] * height_far / clip_shape[cam][1],
      ))

      dof.append(cam_dof)
    
    return dof
