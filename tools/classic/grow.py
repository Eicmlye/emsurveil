import argparse
import geatpy as ea
import logging
import numpy as np
import os

from emsurveil.logger import build_logger
from problems import BaseOCP


def parse_args():
  parser = argparse.ArgumentParser(
    description="The evolution process of generic algorithm. ",
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

  problem = BaseOCP(
    name="Base OCP",
    M=1,
    maxormins=np.array([-1]),
    Dim=3,
    varTypes=np.array([0, 0, 0]),
    lb=np.array([0, 0, 0]),
    ub=np.array([1, 1, 2]),
    lbin=np.array([1, 1, 0]),
    ubin=np.array([1, 1, 0]),
  )
  field = ea.crtfld(
    "RI",
    problem.varTypes,
    problem.ranges,
    problem.borders,
  )
  population = ea.Population("RI", field, 50)

  algo = ea.soea_DE_best_1_bin_templet(problem, population, dirName=args.out_dir)
  algo.MAXGEN = 500
  algo.mutOper.F = 0.5
  algo.recOper.XOVR = 0.7
  algo.logTras = 1
  algo.verbose = True
  algo.drawing = 3

  [best_individual, population] = algo.run()
  best_individual.save(args.out_dir)


if __name__ == "__main__":
  main()