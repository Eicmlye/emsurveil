from emsurveil.envs import BaseOCPEnv
from emsurveil.visibility.camera import BaseCameraCandidates
from emsurveil.visibility.vis_mat import BaseVisMat

class BaseTranslator:
  """
  Args:
  """

  def __init__(
    self,
    cam_cfg: dict,
    env_cfg: dict,
    **kwargs,
  ):
    cam = self.build_cam(cam_cfg, **kwargs)
    env = self.build_env(env_cfg, **kwargs)
    vis_mat = self.build_vis_mat(cam, env, **kwargs)

  def build_cam(self, cam_cfg, **kwargs):
    if (
      not hasattr(cam_cfg, "directions")
      or not hasattr(cam_cfg, "clip_shapes")
      or not hasattr(cam_cfg, "focal_lens")
      or not hasattr(cam_cfg, "resolutions")
      or not hasattr(cam_cfg, "horizontal_resols")
      or not hasattr(cam_cfg, "vertical_resols")
    ):
      raise ValueError("Missing camera settings.")
    cam_type = getattr(cam_cfg, "type", BaseCameraCandidates)
    cam = cam_type(
      cam_cfg.directions,
      cam_cfg.clip_shapes,
      cam_cfg.focal_lens,
      cam_cfg.resolutions,
      cam_cfg.horizontal_resols,
      cam_cfg.vertical_resols,
      **kwargs,
    )

    return cam
  
  def build_env(self, env_cfg, **kwargs):
    if (
      not hasattr(env_cfg, "shape")
      or not hasattr(env_cfg, "occupacy")
      or not hasattr(env_cfg, "voxel_len")
      or not hasattr(env_cfg, "targets")
    ):
      raise ValueError("Missing environmental settings.")
    env_type = getattr(env_cfg, "type", BaseOCPEnv)
    env = env_type(
      env_cfg.shape, env_cfg.occupacy, env_cfg.voxel_len, env_cfg.targets, **kwargs
    )

    return env
  
  def build_vis_mat(self, cam, env, **kwargs):
    vis_mat_type = getattr(kwargs, "vis_mat_type", BaseVisMat)
    vis_mat = vis_mat_type(cam, env, **kwargs)
