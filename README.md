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

Visibility matrices `VisMat` are computed from environmental distribution and camera settings. 

### `envs/`

`Environment`s collect the environmental arguments and translate them to OCP concerning values.

### `problems/`

`geatpy` `Problem`s mainly build optimization problems.

## OCP requirements

In this package, **`[width, height, depth]` corresponds to `[y, z, x]` coordinates of the space**. 
```text
                                              height
                                    width     |
                                         \    |
                                          \   |
                                           \  |
                                            \ |
watcher's sight     ------>                  \|_____________depth
```
The following sheet lists all the necessary arguments to start a OCP problem:

| Categories | Arguments | Definitions |
| :---: | :---: | --- |
| `Camera` | `direction` | `[span, tilt]` angles of cameras, both of which taking `x` axis as $0$ rad.  |
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