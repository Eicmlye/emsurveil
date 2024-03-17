import argparse
import geatpy as ea
import logging
import os

from emsurveil.logger import build_logger
from emsurveil.problems._base_ import BaseOCPProblem
from configs import Config


def parse_args():
  parser = argparse.ArgumentParser(
    description="The evolution process of generic algorithm. "
  )

  parser.add_argument("--config", type=str, help="Path of the configuration file.")
  parser.add_argument(
    "--out-dir",
    type=str,
    default="./output/",
    help="Path to save output files."
  )

  args = parser.parse_args()
  return args


def main():
  args = parse_args()
  os.makedirs(args.out_dir, exist_ok=True)

  logger = build_logger(args.out_dir, level=logging.INFO)

  cfg = Config.fromfile(args.config)

  problem = BaseOCPProblem(cfg["cameras"], cfg["env"], logger=logger)
  field = ea.crtfld(
    cfg["encoding"], problem.is_discrete_var, problem.ranges, problem.borders
  )
  population = ea.Population(cfg["encoding"], field, cfg["population_size"])

  algo = ea.soea_DE_best_1_bin_templet(
    problem,
    population,
    MAXGEN=cfg["total_generations"],
    logTras=cfg["logger_cfg"]["interval"],
    verbose=True,
    drawing=1,
    dirName=args.out_dir,
  )

  algo.mutOper.F = 0.5
  algo.recOper.XOVR = cfg["crossover_prob"]
  
  best_individual, _ = algo.run()
  best_individual.save(args.out_dir)


if __name__ == "__main__":
  main()