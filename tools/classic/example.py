import argparse
import geatpy as ea
import logging
import numpy as np
import os

from emsurveil.logger import build_logger
from emsurveil.problems._base_.example import ExampleProblem


def parse_args():
  parser = argparse.ArgumentParser(
    description="An example program for GA. "
  )

  parser.add_argument(
    "--out-dir",
    type=str,
    default="./emsurveil_example_output/",
    help="Path to save output files."
  )

  args = parser.parse_args()
  return args


def main():
  args = parse_args()
  os.makedirs(args.out_dir, exist_ok=True)

  EMLOG = build_logger(args.out_dir, level=logging.INFO)

  problem = ExampleProblem(
    name="Example problem",
    is_maximize_target=[-1],
    is_discrete_var=[0, 0, 0],
    lbound=[0, 0, 0],
    ubound=[1, 1, 2],
    lborder=[1, 1, 0],
    uborder=[1, 1, 0],
  )
  field = ea.crtfld(
    "RI",
    problem.is_discrete_var,
    problem.ranges,
    problem.borders,
  )
  population = ea.Population("RI", field, 50)

  algo = ea.soea_DE_best_1_bin_templet(
    problem,
    population,
    dirName=args.out_dir,
  )
  algo.MAXGEN = 500
  algo.mutOper.F = 0.5
  algo.recOper.XOVR = 0.7
  algo.logTras = 1
  algo.verbose = True
  algo.drawing = 1

  [best_individual, population] = algo.run()
  best_individual.save(args.out_dir)


if __name__ == "__main__":
  main()