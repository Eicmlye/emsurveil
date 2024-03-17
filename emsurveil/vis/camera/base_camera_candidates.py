import numpy as np

from emsurveil.vis.camera import BaseSingleCamera


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
    costs: list[float],
  ):
    assert (
      len(directions) == len(clip_shapes) == len(focal_lens) == len(resolutions)
      and len(focal_lens) == len(horizontal_resols) == len(vertical_resols)
    ), "Inconsistent argument length. "
    
    self.__candidates = []
    for cam_index in range(len(directions)):
      cam = BaseSingleCamera(
        directions[cam_index],
        clip_shapes[cam_index],
        focal_lens[cam_index],
        resolutions[cam_index],
        horizontal_resols[cam_index],
        vertical_resols[cam_index],
        costs[cam_index],
      )
      self.__candidates.append(cam)
    self.__costs = np.array(costs)

  @property
  def candidates(self) -> list[BaseSingleCamera]:
    return self.__candidates

  @property
  def costs(self):
    return self.__costs
  

  def __len__(self):
    return len(self.candidates)
  

if __name__ == "__main__":
  cls = BaseCameraCandidates([[1,2]],[[1,2]],[1],[[1,2]],[[1,2]],[[1,2]])
  import pdb; pdb.set_trace()