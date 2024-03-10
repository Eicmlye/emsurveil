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

This directory computes visibility matrix from known obstacle distribution and camera settings. 

### `envs/`

This directory translates the OCP representation of the problem to a geatpy one, i.e., to an optimization problem. Envs can be considered as a interface between OCP and SCP. 

### `problems/`

This directory mainly builds geatpy optimization problems.