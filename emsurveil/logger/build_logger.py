"""
See https://zhuanlan.zhihu.com/p/476549020 for detail usages.
"""

import logging
import os
import time

STANDARD_LOG = "[%(asctime)s][%(levelname)s] IN %(pathname)s, Line %(lineno)d: %(message)s"

def build_logger(
  dir_name: str,
  level: int=logging.DEBUG,
  file_name: str=time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".log",
  format: str=STANDARD_LOG,
):
  logger = logging.getLogger()
  logger.setLevel(level)
  logger_format = logging.Formatter(format)

  cmd_handler = logging.StreamHandler()
  cmd_handler.setLevel(level)
  cmd_handler.setFormatter(logger_format)
  
  file_handler = logging.FileHandler(os.path.join(dir_name, file_name))
  file_handler.setLevel(level)
  file_handler.setFormatter(logger_format)

  logger.addHandler(cmd_handler)
  logger.addHandler(file_handler)

  return logger