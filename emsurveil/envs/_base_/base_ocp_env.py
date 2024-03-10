class BaseOCPEnv:
  """
  # Args:

    - shape (list[int]): [width, height, depth] of the space in voxels.

    - occupacy (list[int]): 1 indicating a occupied voxel while 0 means an
        empty one.

    - voxel_len (float): length of sides of voxels in meters.

    - targets (list[int]): positions of target points. Default value is
        `None`, which means all points are targets. 
  """

  def __init__(
    self,
    shape: list[int],
    occupacy: list[int],
    voxel_len: float,
    targets: list[int]=None,
  ):
    if len(shape) != 3:
      raise ValueError(
        "`shape` should be [width, height, depth] of the space."
      )
    if not (
      len(occupacy) == len(targets) == shape[0] * shape[1] * shape[2]
    ):
      raise ValueError("Inconsistent voxel numbers among inputs. ")
    if voxel_len <= 0:
      raise ValueError(f"{voxel_len} is an illegal voxel side length. ")

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