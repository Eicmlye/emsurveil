import numpy as np

def squential_space_to_cartesian(shape: list[int]) -> list[np.ndarray]:
  """
  Translate sequential space to cartesian. 

  # Args: 

    - shape (list[int]): [width, height, depth] of the space in voxels.
  """

  cartesian = []
  for w in range(shape[0]):
    for h in range(shape[1]):
      for d in range(shape[2]):
        cartesian.append(np.array([w, h, d]))
  
  return cartesian

def normalize_vector(vector: np.ndarray) -> np.ndarray:
  """
  Compute the unit vector with the same direction of `vector`.
  """

  return vector / np.linalg.norm(vector)