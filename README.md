# Welcome to `emsurveil`

## Description

This repository is a Python implementation of *Camera Placement Plan Evaluation System for Early Warning in Laboratories*. 

## Installation

```bash
cd emsurveil/ # change to project directory
pip install -e . # install the project in editable mode
```

## Usage

### `visibility/`

The main goal of this directory is to compute visibility matrix from voxel occupacy conditions. 

### `envs/`

The main goal of this directory is to translate the OCP representation of the problem to a geatpy one, i.e., to an optimization problem. Envs can be considered as a interface between OCP and SCP. 

### `problems/`

This directory mainly solves geatpy optimization problems.