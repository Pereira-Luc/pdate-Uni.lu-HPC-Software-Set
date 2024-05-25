# Update Uni.lu HPC Software Set

## Overview

The EasyBuild Module Tool consists of two Python scripts that allow users to search for specified software modules and toolchains (`foss-2023a` and `intel-2023a`) using EasyBuild and to install them on the Uni.lu cluster. 

- [**`easybuild_module_search.py`**](easybuild_module_search.py): \
  This script provides options to either create a file with installation paths or retrieve all dependencies and count them for debugging purposes.
- [**`easybuild_create_slurm.py`**](easybuild_create_slurm.py): \
  This script creates a batch script according to the specified and found modules from the previous search, which can then be used to install them.

## Features

- Search for specified software modules using EasyBuild. \
  Current modules include: 
  - `GROMACS`
  - `OpenFOAM`
  - `ParaView`
  - `gnuplot`
  - `Julia` 
  - `Rust`
  - `TensorFlow`
  - `PyTorch`
  - `PyTorch-Lightning` 
  - `Spark`
  - `Armadillo` 
  - `GDAL` 
  - `GSL` 
  - `Eigen`
  - `ABAQUS` 
  - `R` 
  - `gmsh` 
  - `Keras` 
  - `Horovod` 
  - `Neper` 
  - `trimesh`
- Filter search results with a specified toolchain version:
  - `foss-2023a`
  - `intel-2023a`
  - `independent`
- Choose between creating a file with installation paths or retrieving all modules and dependencies for debugging purposes.
- Create a batch script based on the found modules.
- Install all modules with the specified toolchain on the Uni.lu cluster.

## Connect to the Aion-cluster

1. Connect to the access node of the Aion-cluster.
2. Connect to a compute node:
```
salloc -p interactive --qos debug --reservation=hpc_software_5d07 --time=2:00:00`
```
3. Clone the repository:
```
git clone git@github.com:Pereira-Luc/pdate-Uni.lu-HPC-Software-Set.git
```

## Prerequisites

1. Load a Python module (e.g. `lang/Python/3.8.6-GCCcore-10.2.0`):
```
module load lang/Python/3.8.6-GCCcore-10.2.0
```
2. Load an EasyBuild module (e.g. tools/EasyBuild/4.9.0):
```
module load tools/EasyBuild/4.9.0
```
3. Since we will need EasyBuild 4.9.1, install the latest release if you have not already done so:
```
eb --install-latest-eb-release
```
4. And load it afterwards:
```
module load tools/EasyBuild/4.9.1
```

## Installation of modules with toolchain `foss-2023a` and `intel-2023a`

1. Run the module search script using the following command:
```
python easybuild_module_search.py
```

2. Follow the on-screen prompts to specify the desired version of modules that have multiple versions available. 
   For our purposes you can choose each version arbitrarily.

3. Once the search is complete, the results will be saved to the output file `module_search_results.txt`.

4. Run the slurm creation script using the following command:
```
python easybuild_create_slurm.py
```

5. Run the newly created slurm script on the cluster to install the found modules using the following command:
```
sbatch install_modules.sh
```

6. After this is done, we can proceed with the installation of the modules with the toolchaín `intel-2023a`. \
  Change the toolchain version at the beginning of [`easybuild_module_search.py`](easybuild_module_search.py) to `intel` and repeat the same commands.

## Installation of modules without dependency on the toolchain

MISSING

## Options

You can change certain parameters at the beginning of the file [`easybuild_module_search.py`](easybuild_module_search.py):

- `toolchain`: \
  Toolchain version to use in the search. Either set to `foss` for `foss-2023a` or `intel` for `intel-2023a`. \
  Default: `foss`
- `create_install_file`: \
  Set to `True` to create a file with installation paths or `False` to retrieve all dependencies for debugging purposes.\
  Default: `True`
