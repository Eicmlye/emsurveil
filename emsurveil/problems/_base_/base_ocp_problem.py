import geatpy as ea

from emsurveil.envs import BaseOCPEnv
from emsurveil.translator import BaseTranslator
from emsurveil.visibility.camera import BaseCameraCandidates
from emsurveil.visibility.vis_mat import BaseVisMat


class BaseOCPProblem(ea.Problem):
  """
  Args:
    is_maximize_target (np.ndarray):  1 indicating maximization while -1 indicating
      minimization. 
    is_discrete_var (np.ndarray): 0 indicating a continuous variable while 1
      indicating a discrete one.
    lbound (np.ndarray): lower bound of decision variable.
    ubound (np.ndarray): upper bound of decision variable.
    lborder (np.ndarray): 0 means a open half-interval at lower bound while 1 means
      a closed one.
    uborder (np.ndarray): 0 means a open half-interval at upper bound while 1 means
      a closed one.
    name (str): name of the problem.
  """

  def __init__(
    self,
    cam_cfg: dict,
    env_cfg: dict,
    **kwargs,
  ):
    self.__cam = self.build_cam(cam_cfg, **kwargs)
    self.__env = self.build_env(env_cfg, **kwargs)
    self.__vis_mat = self.build_vis_mat(self.cameras, self.env, **kwargs)
    self.__translator = self.build_translator(
      self.cameras, self.env, self.vis_mat, **kwargs
    )

    (
      is_maximize_target, is_discrete_var, lbound, ubound, lborder, uborder
    ) = self.translator.translation["var"]

    super().__init__(
      name=getattr(kwargs, "name", "Base problem"),
      M=len(is_maximize_target),
      maxormins=is_maximize_target,
      Dim=len(is_discrete_var),
      varTypes=is_discrete_var,
      lb=lbound,
      ub=ubound,
      lbin=lborder,
      ubin=uborder,
    )
  

  @property
  def cameras(self):
    return self.__cam
  
  @property
  def env(self):
    return self.__env
  
  @property
  def vis_mat(self):
    return self.__vis_mat
  
  @property
  def translator(self):
    return self.__translator


  def build_cam(self, cam_cfg: dict, **kwargs):
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
    cameras = cam_type(
      cam_cfg.directions,
      cam_cfg.clip_shapes,
      cam_cfg.focal_lens,
      cam_cfg.resolutions,
      cam_cfg.horizontal_resols,
      cam_cfg.vertical_resols,
      **kwargs,
    )

    return cameras
  
  def build_env(self, env_cfg: dict, **kwargs):
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
  
  def build_vis_mat(self, cameras: BaseCameraCandidates, env: BaseOCPEnv, **kwargs):
    vis_mat_type = getattr(kwargs, "vis_mat_type", BaseVisMat)
    vis_mat = vis_mat_type(cameras, env, **kwargs)

    return vis_mat

  def build_translator(
    self, cameras: BaseCameraCandidates, env: BaseOCPEnv, vis_mat: BaseVisMat, **kwargs
  ):
    translator_type = getattr(kwargs, "translator_type", BaseTranslator)
    translator = translator_type(cameras, env, **kwargs)

    return translator


  # Rename badly formatted attributes in geatpy and make them kind of read-only
  @property
  def len_target(self):
    return self.M

  @property
  def is_maximize_target(self):
    return self.maxormins

  @property
  def len_var(self):
    return self.Dim
  
  @property
  def is_discrete_var(self):
    return self.varTypes
  
  # self.ranges can be changed but it's defined according to
  # lb and ub, which is weird but we will leave this bug alone.
  # TODO: reconstruct range attribute and maybe the whole geatpy.
  @property
  def lbound(self):
    return self.lb
  
  @property
  def ubound(self):
    return self.ub
  
  @property
  def lborder(self):
    return self.borders[0]
  
  @property
  def uborder(self):
    return self.borders[1]
    

  def aimFunc(self, pop: ea.Population, **kwargs):
    pop.ObjV, pop.CV = self.translator.translate_aim_and_constraints(
      pop, self.cameras, self.env, self.vis_mat, **kwargs
    )
  