import math
import numpy as np
from tqdm import tqdm

from emsurveil.visibility import (
  normalize_vector,
  squential_space_to_cartesian,
)

class VisMat:
  """
  # Args: 

    - shape (list[int]): [width, height, depth] of the space in voxels.

    - occupacy (list[int]): 1 indicating a occupied voxel while 0 means an
        empty one.

    - cam_direction (list[list[float, float]]): the direction of cams in
        radians.

    - cam_dof (list[list[float, float]]): the DoFs of cameras in meters.

    - cam_horizontal_angle (list[float]): the horizontal fov angles of
        cameras in radians.

    - cam_vertical_angle (list[float]): the vertical fov angles of cameras
        in radians.

    - voxel_len (float): length of sides of voxels in meters.

    - sample_step (float): length of a sample step in voxels.

  # Attributes:

    - value (np.ndarray): a matrix of dimension num_voxel^2.
  """

  def __init__(
    self,
    shape: list[int],
    occupacy: list[int],
    cam_direction: list[list[float, float]],
    cam_dof: list[list[float, float]],
    cam_horizontal_angle: list[float],
    cam_vertical_angle: list[float],
    voxel_len: float,
    sample_step: float=0.2,
  ):
    self.value = self._compute_vis(
      shape,
      occupacy,
      cam_direction,
      cam_dof,
      cam_horizontal_angle,
      cam_vertical_angle,
      voxel_len,
      sample_step,
    )

  def _compute_vis(
    self,
    shape: list[int],
    occupacy: list[int],
    cam_direction: list[list[float, float]],
    cam_dof: list[float],
    cam_horizontal_angle: list[float],
    cam_vertical_angle: list[float],
    voxel_len: float,
    sample_step: float=0.2,
  ):
    """
    Compute the visibility matrix, taking [depth, width, height] as
    [x, y, z] axes. Currently we do not really care about the actual
    target positions, but just compute the whole viewshed.
    
    # Args: 

      - shape (list[int]): [width, height, depth] of the space.

      - occupacy (list[int]): 1 indicating a ocupied voxel while 0 means
          an empty one.

      - cam_direction (list[list[float, float]]): the direction of cams.

      - cam_dof (list[list[float, float]]): the DoFs of cameras in meters.

      - cam_horizontal_angle (list[float]): the horizontal fov angles of
          cameras.

      - cam_vertical_angle (list[float]): the vertical fov angles of
          cameras.

      - voxel_len (float): length of sides of voxels in meters.

      - sample_step (float): sample step when checking if sight of view is
          blocked by obstacles. Camera and target positions are not
          considered sample points. The unit of sample_step is voxel.
    """

    num_voxel = shape[0] * shape[1] * shape[2]
    cartesian = squential_space_to_cartesian(shape)
    vis = np.ones([num_voxel, num_voxel])

    # Compute angles of view from cams to targets, the first column
    # indicates horizontal angles and the second indicates vertical ones.
    for cam in tqdm(
      range(num_voxel),
      ascii=True,
      desc="Camera pos checking",
    ):
      if cam_dof[cam][1] == 0:
        for tar in tqdm(
          range(num_voxel),
          ascii=True,
          desc="Target visibility checking",
        ):
          vis[tar][cam] = 0
        continue
      
      # accessible camera pos
      cam_coord = cartesian[cam]
      for tar in tqdm(
        range(num_voxel),
        ascii=True,
        desc="Target visibility checking",
      ):
        tar_coord = cartesian[tar]
        diffs = tar_coord - cam_coord

        if (
          not self._check_angle(
            diffs,
            cam_direction[cam],
            cam_horizontal_angle[cam],
            cam_vertical_angle[cam],
          ) or not self._check_distance(diffs, voxel_len, cam_dof[cam])
        ):
          vis[tar][cam] = 0
          continue

        step = sample_step * normalize_vector(diffs)
        sample = cam_coord + step
        next_sample = sample + step
        while (
          (sample[0] - tar_coord[0]) * (
            next_sample[0] - tar_coord[0]
          ) > 0 or next_sample[0] - tar_coord[0] == 0
        ):
          # The target point is not sampled.
          if self._check_obstacles(shape, occupacy, sample):
            vis[tar][cam] = 0
            break

          sample += step
          next_sample = sample + step
    
    print("Visibility matrix successfully built. ")


  def _compute_aov_single(self, diffs: list[int]):
    """
    Compute angle of view of a single pair of camera and target in
    radians.
    """

    horizontal = math.asin(
      diffs[0] / math.sqrt(diffs[0] ** 2 + diffs[2] ** 2)
    )
    vertical = math.asin(diffs[1] / np.linalg.norm(diffs))

    if diffs[0] > 0 and diffs[2] < 0:
      horizontal = math.pi - horizontal
    if diffs[0] < 0 and diffs[2] > 0:
      horizontal = -math.pi - horizontal
    
    return [horizontal, vertical]
  
  def _check_angle(
    self,
    diffs: np.ndarray,
    single_cam_direction: list[float],
    single_cam_horizontal_angle: float,
    single_cam_vertical_angle: float,
  ):
    """
    Check if target is in the angle range of FoV.
    """
    
    angle_of_view = self._compute_aov_single(diffs)

    diff_horizontal = angle_of_view[0] - single_cam_direction[0]
    if (
      diff_horizontal < -single_cam_horizontal_angle / 2
      or diff_horizontal > single_cam_horizontal_angle / 2
    ):
      return False
    
    diff_vertical = angle_of_view[1] - single_cam_direction[1]
    if (
      diff_vertical < -single_cam_vertical_angle / 2
      or diff_vertical > single_cam_vertical_angle / 2
    ):
      return False
    
    return True

  def _check_distance(
    self, diffs: np.ndarray, voxel_len: float, single_cam_dof: list[float]
  ):
    """
    Check if the target is in the range of DoF.
    """
    
    dist = np.linalg.norm(diffs) * voxel_len
    return dist >= single_cam_dof[0] and dist <= single_cam_dof[1]
  
  def _check_obstacles(
    self, shape: list[int], occupacy: list[int], sample: np.ndarray
  ):
    """
    Check if the sample point is in any occupied voxel.
    """

    voxel = [round(sample[i]) for i in range(len(sample))]
    if occupacy[shape[0] * voxel[0] + shape[1] * voxel[1] + voxel[2]] > 0:
      return True

    # If the sample point is on the surface of voxels, any occupied voxel
    # will make the sample point blocked.
    if (
      sample[0] % 1 == 0.5
      and occupacy[
        shape[0] * (voxel[0] - 1) + shape[1] * voxel[1] + voxel[2]
      ] > 0
    ):
      return True
    if (
      sample[1] % 1 == 0.5
      and occupacy[
        shape[0] * voxel[0] + shape[1] * (voxel[1] - 1) + voxel[2]
      ] > 0
    ):
      return True
    if (
      sample[2] % 1 == 0.5
      and occupacy[
        shape[0] * voxel[0] + shape[1] * voxel[1] + voxel[2] - 1
      ] > 0
    ):
      return True
    
    return False
