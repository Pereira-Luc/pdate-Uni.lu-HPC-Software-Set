# Update Uni.lu HPC Software Set

## Overview

The EasyBuild Module Tool consists of two Python scripts that allow users to search for specified software modules and 
toolchains (`foss-2023a`, `intel-2023a` and `independent`) using EasyBuild and to install them on the Uni.lu cluster. 

- [**`easybuild_module_search.py`**](easybuild_module_search.py): \
  This script provides options to either create a file with installation paths or retrieve all dependencies and count 
  them for debugging purposes.
- [**`easybuild_create_slurm.py`**](easybuild_create_slurm.py): \
  This script creates a batch script according to the specified and found modules from the previous search, which can 
  then be used to install them or try a dry-run first.

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
- Create a batch script based on the found modules to either install the modules or use a dry-run first.
- Install all modules with the specified toolchain on the Uni.lu cluster.

## Options

You can change certain parameters at the beginning of the file [`easybuild_module_search.py`](easybuild_module_search.py):

- `toolchain`: \
  Toolchain version to use in the search. Either set to `foss` for `foss-2023a`, `intel` for `intel-2023a` or 
  `independent` for some modules without specific toolchain versions. \
  Default: `foss`
- `create_install_file`: \
  Set to `True` to create a file with installation paths or `False` to retrieve all dependencies for debugging purposes.\
  Default: `True`

Similarly, you are able to change some arguments at the top of [`easybuild_create_slurm.py`](easybuild_create_slurm.py):

- `toolchain`: \
  Toolchain version to use for the installation. Either set to `foss` for `foss-2023a`, `intel` for `intel-2023a` or 
  `independent` for some modules without specific toolchain versions. \
  Default: `foss`
- `job_cores`: \
  Number of CPU cores per module installation job. \
  Default: `4`
- `max_walltime`: \
  Max wall time in hours per module installation job. \
  Default: `2`
- `dry_run`: \
  Set to `True` to use an EasyBuild dry run for debugging purposes or set to `False` to install modules on the cluster. \
  Default: `False`

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

## Installing/Upgrading EasyBuild

1. Use `module` to find the currently available version of EasyBuild and load it (e.g. tools/EasyBuild/4.9.0):
```
module load tools/EasyBuild/4.9.0
```
2. Check the current version of EasyBuild:
```
eb --version
```
3. Since we will need EasyBuild 4.9.1, install the latest release if you have not already done so:
```
eb --install-latest-eb-release
```
4. And load it afterwards:
```
module load tools/EasyBuild/4.9.1
```
5. To make the software installed by EasyBuild searchable with `module`, update the Lmod search path accordingly:
```
module use "${EASYBUILD_PREFIX}/modules/all"
```
6. To make this change permanent, add the following lines at the end of your `~/.bashrc` file:
```
if command -v module >/dev/null 2>&1 ; then
    module use "${EASYBUILD_PREFIX}/modules/all"
fi
```

## Installation of modules with toolchain `foss-2023a`, `intel-2023a` and `independent`

1. We are going to start with the installation of the `foss-2023` toolchain first.\
   Run the module search script using the following command 
   (depending on your python configuration you may need to use `python3` for the following sections):
```
python easybuild_module_search.py
```

2. Follow the on-screen prompts to specify the desired version of modules that have multiple versions available. 
   For our purposes you can choose each version arbitrarily.

3. Once the search is complete, the results will be saved to the output file `module_search_results_foss.txt`.

4. Run the slurm creation script using the following command:
```
python easybuild_create_slurm.py
```

5. Run the newly created slurm script on the cluster to install the found modules using the following command:
```
sbatch install_modules_foss.sh
```
   This is going to create multiple batch scripts, installing all the modules and their dependencies. The log files can be found in the folder `eb_logs_foss`.

6. After this is done, we can proceed with the installation of the modules with the toolchaín `intel-2023a` and `independent`. \
   Change the toolchain version at the beginning of [`easybuild_module_search.py`](easybuild_module_search.py) and 
   [`easybuild_create_slurm.py`](easybuild_create_slurm.py)  to `intel` or `independent` and repeat the same commands. \
   The output file name is now going to be `module_search_results_<toolchain>.txt`, the slurm script `install_modules_<toolchain>.sh`
   and the log folder `eb_logs_<toolchain>`.

## Expected Output

Once everything is installed, you should be able to find all the new modules in your home directory by using `module`. 
Due to multiple dependencies and the availability of the cluster nodes, this could take several hours.




