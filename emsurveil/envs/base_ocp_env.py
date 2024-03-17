import numpy as np

class BaseOCPEnv:
  """
  Args:
    shape (list[int]): [width, height, depth] of the space in voxels.
    occupacy (np.ndarray): 1 indicating a occupied voxel while 0 means an empty one.
    voxel_len (float): length of sides of voxels in meters.
    targets (np.ndarray): positions of target points. Default value is `None`, which
      means all points are targets.
  
  Attributes:
    shape (list[int]): [width, height, depth] of the space in voxels.
    num_voxel(int): the total number of voxels in the concerning space.
    occupacy (np.ndarray): 1 indicating a occupied voxel while 0 means an empty one.
    voxel_len (float): length of sides of voxels in meters.
    targets (np.ndarray): positions of target points. Default value is `None`, which
      means all points are targets.
  """

  def __init__(
    self,
    shape: list[int],
    occupacy: np.ndarray,
    voxel_len: float,
    targets: np.ndarray=None,
  ):
    assert len(shape) == 3, "`shape` should be [width, height, depth] of the space."
    assert (
      len(occupacy) == len(targets) == shape[0] * shape[1] * shape[2]
    ), "Inconsistent voxel numbers among inputs. "
    assert voxel_len > 0, "voxel_len should be positive float. "

    self.__shape = shape
    self.__occupacy = occupacy
    self.__voxel_len = voxel_len
    self.__targets = targets


  @property
  def shape(self):
    return self.__shape
  
  @property
  def num_voxel(self):
    return self.shape[0] * self.shape[1] * self.shape[2]

  @property
  def occupacy(self):
    return self.__occupacy

  @property
  def voxel_len(self):
    return self.__voxel_len

  @property
  def targets(self):
    return self.__targets
  