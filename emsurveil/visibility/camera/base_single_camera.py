import logging
import math


class BaseSingleCamera:
  """
  # Args:

    - direction (list[float]): the [span, tilt] direction of the camera in
        radians.

    - clip_shape (list[float]): the [width, height] of the clip in meters.

    - focal_len (float): the focal length of the camera in meters.

    - resolution (list[float]): [width, height] resolutions of images shot
        by the camera in pixels.

    - horizontal_resol (list[float]): [min, max] of the horizontal
        resolution requirements for the camera in pixels per meter.

    - vertical_resol (list[float]): [min, max] of the vertical resolution
        requirements for the camera in pixels per meter.

  # Attributes:

    - direction (list[float]): the [span, tilt] direction of the camera in
        radians.

    - dof (list[float]): the [near, far] DoFs of the camera in meters.

    - horizontal_angle (float): the horizontal FoV angle of the camera in
        radians.

    - vertical_angle (float): the vertical FoV angle of the camera in
        radians.
  """

  def __init__(
    self,
    direction: list[float],
    clip_shape: list[float],
    focal_len: float,
    resolution: list[float],
    horizontal_resol: list[float],
    vertical_resol: list[float],
  ):
    if len(direction) == 1:
      raise ValueError("Two directional angles are required for [span, tilt].")
    if len(clip_shape) == 1 or len(resolution) == 1:
      raise ValueError("Two lengths are required for [width, height].")
    if len(horizontal_resol) == 1 or len(vertical_resol) == 1:
      raise ValueError("Two resolution values are required for [min, max].")
    
    if (
      len(direction) > 2
      or len(clip_shape) > 2
      or len(resolution) > 2
      or len(horizontal_resol) > 2
      or len(vertical_resol) > 2
    ):
      logging.warn(
        "`list` arguments with length longer than 2 will be treated as if "
        "they are of length 2."
      )
    
    self.__direction = direction
    self.__dof = self._compute_dof(
      clip_shape,
      focal_len,
      resolution,
      horizontal_resol,
      vertical_resol,
    )
    self.__horizontal_angle = 2 * math.atan(clip_shape[0] / focal_len / 2)
    self.__vertical_angle = 2 * math.atan(clip_shape[1] / focal_len / 2)


  @property
  def direction(self):
    return self.__direction

  @property
  def dof(self):
    return self.__dof

  @property
  def horizontal_angle(self):
    return self.__horizontal_angle

  @property
  def vertical_angle(self):
    return self.__vertical_angle

  def _compute_dof(
    self,
    clip_shape: list[float],
    focal_len: float,
    resolution: list[float],
    horizontal_resol: list[float],
    vertical_resol: list[float],
  ):
    """
    # Args:

      - clip_shape (list[float]): the [width, height] of the clip in meters.

      - focal_len (float): the focal length of the camera in meters.

      - resolution (list[float]): [width, height] resolutions of images shot
          by the camera in pixels.

      - horizontal_resol (list[float]): [min, max] of the horizontal
          resolution requirements for the camera in pixels per meter.

      - vertical_resol (list[float]): [min, max] of the vertical
          resolution requirements for the camera in pixels per meter.
    """
    dof = []
    # near limit of DoF
    width_near = resolution[0] / horizontal_resol[1]
    height_near = resolution[1] / vertical_resol[1]
    dof.append(max(
      focal_len * width_near / clip_shape[0],
      focal_len * height_near / clip_shape[1],
    ))
    # far limit of DoF
    width_far = resolution[0] / horizontal_resol[0]
    height_far = resolution[1] / vertical_resol[0]
    dof.append(min(
      focal_len * width_far / clip_shape[0],
      focal_len * height_far / clip_shape[1],
    ))
    
    return dof
