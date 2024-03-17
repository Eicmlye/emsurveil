import logging
import math


class BaseSingleCamera:
  """
  Args:
    direction (list[float]): the [span, tilt] direction of the camera in radians.
    clip_shape (list[float]): the [width, height] of the clip in meters.
    focal_len (float): the focal length of the camera in meters.
    resolution (list[float]): [horizontal, vertical] resolutions of images shot by the
      camera in pixels.
    horizontal_resol (list[float]): [min, max] of the horizontal resolution
      requirements for the camera in pixels per meter.
    vertical_resol (list[float]): [min, max] of the vertical resolution requirements
      for the camera in pixels per meter.

  Attributes:
    direction (list[float]): the [span, tilt] direction of the camera in radians.
    dof (list[float]): the [near, far] DoFs of the camera in meters.
    horizontal_angle (float): the horizontal FoV angle of the camera in radians.
    vertical_angle (float): the vertical FoV angle of the camera in radians.
  """

  def __init__(
    self,
    direction: list[float],
    clip_shape: list[float],
    focal_len: float,
    resolution: list[float],
    horizontal_resol: list[float],
    vertical_resol: list[float],
    cost: float,
  ):
    if direction is None or len(direction) < 2:
      raise ValueError("Two directional angles are required for [span, tilt].")
    if (
      None in [clip_shape, resolution] or len(clip_shape) < 2 or len(resolution) < 2
    ):
      raise ValueError("Two lengths are required for [width, height].")
    if (
      None in [horizontal_resol, vertical_resol] 
      or len(horizontal_resol) < 2
      or len(vertical_resol) < 2
    ):
      raise ValueError("Two resolution values are required for [min, max].")
    
    if (
      len(direction) > 2
      or len(clip_shape) > 2
      or len(resolution) > 2
      or len(horizontal_resol) > 2
      or len(vertical_resol) > 2
    ):
      logging.warn(
        "`list` arguments with length longer than 2 will be treated as if they "
        "were of length 2."
      )
    if (
      horizontal_resol[0] >= horizontal_resol[1]
      or vertical_resol[0] >= vertical_resol[1]
    ):
      logging.warn(
        "Resolution requirements are supposed to be in [min, max] format, but some "
        "minimum appears to be not less than the corresponding maximum. This results "
        "in illegal position for camera. "
      )
    
    self.__direction = direction
    self.__dof = self._compute_dof(
      clip_shape, focal_len, resolution, horizontal_resol, vertical_resol
    )
    self.__horizontal_angle = 2 * math.atan(clip_shape[0] / focal_len / 2)
    self.__vertical_angle = 2 * math.atan(clip_shape[1] / focal_len / 2)
    self.__cost = cost


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
  
  @property
  def cost(self):
    return self.__cost
  
  @property
  def is_available(self):
    """
    DoF indicates whether this position is available. If DoF == [0, 0], the camera
    cannot see anything and is an illegal position. 
    """

    return self.__dof[1] == 0
  

  def _compute_dof(
    self,
    clip_shape: list[float],
    focal_len: float,
    resolution: list[float],
    horizontal_resol: list[float],
    vertical_resol: list[float],
  ):
    """
    Args:
      clip_shape (list[float]): the [width, height] of the clip in meters.
      focal_len (float): the focal length of the camera in meters.
      resolution (list[float]): [width, height] resolutions of images shot by the
        camera in pixels.
      horizontal_resol (list[float]): [min, max] of the horizontal resolution
        requirements for the camera in pixels per meter.
      vertical_resol (list[float]): [min, max] of the vertical resolution
        requirements for the camera in pixels per meter.
    """

    # DoF indicates whether this position is available. If DoF == [0, 0], the camera
    # cannot see anything and is an illegal position. 
    if 0 in clip_shape + horizontal_resol + vertical_resol:
      return [0, 0]

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
