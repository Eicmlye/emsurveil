import argparse
import geatpy as ea
import logging
import os

from emsurveil.logger import build_logger
from emsurveil.problems._base_ import BaseOCPProblem


def parse_args():
  parser = argparse.ArgumentParser(
    description="The evolution process of generic algorithm. "
  )

  parser.add_argument("--config", type=str, help="Path of the configuration file.")
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

  problem = BaseOCPProblem(args.cam_cfg, args.env_cfg, args.extra_cfg)
  field = ea.crtfld(
    args.encoding, problem.is_discrete_var, problem.ranges, problem.borders
  )
  population = ea.Population(args.encoding, field, args.population_size)

  algo = ea.soea_DE_best_1_bin_templet(problem, population, dirName=args.out_dir)

  algo.MAXGEN = args.total_generations
  algo.mutOper.F = 0.5
  algo.recOper.XOVR = 0.7
  algo.logTras = 1
  algo.verbose = True
  algo.drawing = 1
  
  [best_individual, population] = algo.run()
  best_individual.save(args.out_dir)


if __name__ == "__main__":
  main()