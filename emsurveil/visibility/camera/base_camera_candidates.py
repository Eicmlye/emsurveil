from emsurveil.visibility.camera import BaseSingleCamera

class BaseCameraCandidates:
  """
  Attributes:
    candidates (list[BaseSingleCamera])
  """

  def __init__(
    self, 
    directions: list[list[float]],
    clip_shapes: list[list[float]],
    focal_lens: list[float],
    resolutions: list[list[float]],
    horizontal_resols: list[list[float]],
    vertical_resols: list[list[float]],
  ):
    if (
      not len(directions) == len(clip_shapes) == len(focal_lens) == len(resolutions)
      or not len(focal_lens) == len(horizontal_resols) == len(vertical_resols)
    ):
      raise ValueError("Inconsistent argument length. ")
    
    self.__candidates = []
    for cam_index in range(len(directions)):
      cam = BaseSingleCamera(
        directions[cam_index],
        clip_shapes[cam_index],
        focal_lens[cam_index],
        resolutions[cam_index],
        horizontal_resols[cam_index],
        vertical_resols[cam_index],
      )
      self.__candidates.append(cam)

  @property
  def candidates(self) -> list[BaseSingleCamera]:
    return self.__candidates