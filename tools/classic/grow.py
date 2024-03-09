import argparse
import geatpy as ea
import logging
import numpy as np
import os

from emsurveil.logger import build_logger


def parse_args():
  parser = argparse.ArgumentParser(
    description="The evolution process of generic algorithm. "
  )

  parser.add_argument(
    "--out-dir",
    type=str,
    default="./emsurveil_output/",
    help="Path to save output files."
  )

  args = parser.parse_args()
  return args


def main():
  args = parse_args()
  os.makedirs(args.out_dir, exist_ok=True)

  EMLOG = build_logger(args.out_dir, level=logging.INFO)


if __name__ == "__main__":
  main()