# Welcome to `emsurveil`

## Description

This repository is a Python implementation of *Camera Placement Plan Evaluation System for Early Warning in Laboratories*. 

## Installation

```bash
cd emsurveil/ # change to project directory
pip install -e . # install the project in editable mode
```

## Usage

### `vis/`

`Camera`s take intrinsic camera arguments and generates OCP concerning arguments of cameras.

Visibility matrices `VisMat` are computed from environmental distribution and camera settings. 

### `envs/`

`Environment`s collect the environmental arguments and translate them to OCP concerning values.

### `translator/`

`Translator`s translate OCP problems into `geatpy` optimizations.

### `problems/`

`geatpy` `Problem`s mainly build optimization problems.

## OCP requirements

In `emsurveil`, **`[width, height, depth]` corresponds to `[y, z, x]` coordinates of the space**. 
```text
                                            z-height
                                  y-width     |
                                         \    |
                                          \   |
                                           \  |
                                            \ |
watcher's sight     ------>                  \|_____________x-depth
```
The following sheet lists all the necessary arguments to start an OCP problem:

| Categories | Arguments | Definitions |
| :---: | :---: | --- |
| `Camera` | `direction` | `[span, tilt]` angles of cameras, both of which taking `x` axis as $0\ \mathrm{rad}$.  `span` ranges in $[-\pi, \pi)$. |
| `Camera` | `clip_shape` | `[width, height]` of clip sensors in cameras |
| `Camera` | `focal_len` | focal lengths of cameras |
| `Camera` | `resolution` | the `[width, height]` resolutions of images shot by cameras |
| `Camera` | `cost` | the cost to set cameras |
| `User` | `horizontal_resol` | `[min, max]` of the horizontal resolution requirements for cameras |
| `User` | `vertical_resol` | `[min, max]` of the vertical resolution requirements for cameras |
| `Environment` | `shape` | `[width, height, depth]` of the space in voxels |
| `Environment` | `occupacy` | whether a voxel is occupied as an obstacle in space |
| `Environment` | `voxel_len` | the actual length of voxel sides |
| `Environment` | `target` | whether a voxel is considered as a target point |
| `User` | `sample_step` | sample step length when computing visibility matrix |