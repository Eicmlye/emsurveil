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

## OCP requirements

In this package, **`[width, height, depth]` corresponds to `[y, z, x]` coordinates of the space**. The following sheet lists all the necessary arguments to start a OCP problem:

| Categories | Arguments | Definitions |
| :---: | :---: | --- |
| `Camera` | `directions` | `[span, tilt]` angles of cameras, both of which taking `x` axis as $0$ rad.  |
| `Camera` | `clip_shape` | `[width, height]` of clip sensors in cameras |
| `Camera` | `focal_len` | focal lengths of cameras |
| `Camera` | `resolution` | the `[width, height]` resolutions of images shot by cameras |
| `User` | `horizontal_resol` | `[min, max]` of the horizontal resolution requirements for cameras |
| `User` | `vertical_resol` | `[min, max]` of the vertical resolution requirements for cameras |
| `Environment` | `shape` | `[width, height, depth]` of the space in voxels |
| `Environment` | `occupacy` | whether a voxel is occupied as an obstacle in space |
| `Environment` | `voxel_len` | the actual length of voxel sides |
| `Environment` | `target` | whether a voxel is considered as a target point |
| `User` | `sample_step` | sample step length when computing visibility matrix |