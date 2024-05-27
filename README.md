# Update Uni.lu HPC Software Set

## Overview

The EasyBuild Module Tool consists of four Python scripts that allow users to search for specified software modules and 
toolchains (`foss-2023a`, `intel-2023a` and `independent`) using EasyBuild and to install them on the Uni.lu cluster. 

- [**`easybuild_install_toolchains.sh`**](easybuild_install_toolchains.sh): \
  This batch script installs the necessary toolchains for the modules.
- [**`easybuild_module_search.py`**](easybuild_module_search.py): \
  This script provides options to either create a file with installation paths or retrieve all dependencies and count 
  them for debugging purposes.
- [**`easybuild_create_slurm.py`**](easybuild_create_slurm.py): \
  This script creates a batch script according to the specified and found modules from the previous search, which can 
  then be used to install them or try a dry-run first.
- [**`easybuild_validation.py`**](easybuild_validation.py): \
  This script looks at the modules and validates the whole installation.

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
  - `Keras` 
  - `Horovod`
  - `trimesh`
- Filter search results with a specified toolchain version:
  - `foss-2023a`
  - `intel-2023a`
  - `independent`
- Choose between creating a file with installation paths or retrieving all modules and dependencies for debugging purposes.
- Create a batch script based on the found modules to either install the modules or use a dry-run first.
- Install all modules with the specified toolchain on the Uni.lu cluster.
- Validate the installation for its correctness.

## Options

You can change certain parameters at the beginning of the file [`easybuild_module_search.py`](easybuild_module_search.py):

- `toolchain`: \
  Toolchain version to use in the search. Either set to `intel` for `intel-2023a`, `foss` for `foss-2023a` or 
  `independent` for some modules without specific toolchain versions. \
  Default: `intel`
- `create_install_file`: \
  Set to `True` to create a file with installation paths or `False` to retrieve all dependencies for debugging purposes.\
  Default: `True`

Similarly, you are able to change some arguments at the top of [`easybuild_create_slurm.py`](easybuild_create_slurm.py):

- `toolchain`: \
  Toolchain version to use for the installation. Either set to `intel` for `intel-2023a`, `foss` for `foss-2023a` or 
  `independent` for some modules without specific toolchain versions. \
  Default: `intel`
- `job_cores`: \
  Number of CPU cores per module installation job. \
  Default: `8`
- `max_walltime`: \
  Max wall time in hours per module installation job. \
  Default: `5`
- `dry_run`: \
  Set to `True` to use an EasyBuild dry run for debugging purposes or set to `False` to install modules on the cluster. \
  Default: `False`

In the file [`easybuild_validation.py`](easybuild_validation.py) you can set:
- `log_directory`: \
  Path to the directory containing the log files for the validation part. \
  Default: `./eb_logs_intel`

## Connect to the Aion-cluster

1. Connect to the access node of the Aion-cluster.
2. Connect to a compute node:
```
salloc -p interactive --qos debug --reservation=hpc_software_5d07 --time=2:00:00`
```
3. Clone the repository:
```
git clone https://github.com/Pereira-Luc/pdate-Uni.lu-HPC-Software-Set.git 
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

## Preparation of the environment with toolchain `intel-2023a`
1. Before running the main scripts, make sure to install the `intel-2023a` toolchain. \
   For the reproducibility session it is sufficient to only install `intel-2023a`. \
   The installation is done separately to prevent conflicts by running:
```
sbatch easybuild_install_toolchains.sh
```
This script will install the toolchains and dependencies needed and create many jobs that you can monitor with `sq`.
   
Once all the jobs are done you can proceed with the installation of the modules.

If you want to install both toolchains foss and intel add `foss-2023a` inside of easybuild_install_toolchains.sh
like this 
```
EBFILES=("foss-2023a.eb" "intel-2023a.eb")
```
WARNING: DO NOT FORCE KILL THE JOBS! THIS WILL CAUSE THE INSTALLATION TO FAIL AND MAY CAUSE CONFLICTS OR ERRORS.

## Installation of modules with toolchain `intel-2023a`

1. We are going to start with the installation of the `intel-2023` toolchain first.\
   Run the module search script using the following command 
   (depending on your python configuration you may need to use `python3` for the following sections):
```
python easybuild_module_search.py
```

1.1. Optionally You can add the specific toolchain as a parameter like this( default = intel ):
```
python easybuild_module_search.py intel
```

2. Follow the on-screen prompts to specify the desired version of modules that have multiple versions available. 
   For our purposes you can choose each version arbitrarily.

3. Once the search is complete, the results will be saved to the output file `module_search_results_intel.txt`.

4. Run the slurm creation script using the following command:
```
python easybuild_create_slurm.py
```
4.1. Optionally You can add the specific toolchain as a parameter like this (default = intel):
```
python easybuild_create_slurm.py intel
```

5. Run the newly created slurm script on the cluster to install the found modules using the following command:
```
sbatch install_modules_intel.sh
```
   This is going to create multiple batch scripts, that install all the modules and their dependencies. Use `sq` to view them. \
   The log files can be found in the folder `eb_logs_intel`.

  After this is done, we can proceed with the validation of the modules. 

  WARNING: DO NOT FORCE KILL THE JOBS! THIS WILL CAUSE THE INSTALLATION TO FAIL AND MAY CAUSE CONFLICTS OR ERRORS.

  This script will create many .out files that will have any errors that may have occurred during the installation process. 
  Do not remove these files as they are useful for debugging and are required for validation.

## Validation
1. Now that all the files are installed you can validate the installation, but first you need to set your correct log directory path in 
   [`easybuild_validation.py`](easybuild_validation.py).
2. Afterwards, validate by running the following command:
  ```
  python easybuild_validation.py
  ```

  This script will check if all the modules are installed correctly and will output any errors that may have occurred during the installation process. The most common errors are Checksum verification and build failure.
  There were errors when we were testing but we didn't know if it was because of previous conflicts. So there might be a few packets that don't work.

Usually build failures happen because of Checksum errors in dependencies. To fix these errors you need to go to the failed dependency
and update the checksum to the correct one or replace the corrupted dependency. You can find the path to the dependency inside of the dependency.../.out.

## Expected Output

Once everything is installed, you should be able to find all the new modules in your home directory by using `module`. 
Due to multiple dependencies and the availability of the cluster nodes, this could take several hours.

# END OF THE REPRODUCIBILITY SESSION

## Installation with `foss-2023a` 

1. You need to prepare the environment with toolchain `foss-2023a` by changing the version to `foss-2023a` in [`easybuild_install_toolchains.sh`](easybuild_install_toolchains.sh).
2. Change the toolchain version at the beginning of [`easybuild_module_search.py`](easybuild_module_search.py) and 
   [`easybuild_create_slurm.py`](easybuild_create_slurm.py)  to `foss`. \
   The output file name is now going to be `module_search_results_foss.txt`, the slurm script `install_modules_foss.sh`
   and the log folder `eb_logs_foss`.
3. Do not forget to set the right log directory path in [`easybuild_validation.py`](easybuild_validation.py).
4. Repeat the previous commands.

## Installation with `independent`

1. You do not need to prepare the environment for the independent modules.
2. Change the toolchain version at the beginning of [`easybuild_module_search.py`](easybuild_module_search.py) and 
   [`easybuild_create_slurm.py`](easybuild_create_slurm.py)  to `independent`. \
   The output file name is now going to be `module_search_results_independent.txt`, the slurm script `install_modules_independent.sh`
   and the log folder `eb_logs_independent`.
3. Do not forget to set the right log directory path in [`easybuild_validation.py`](easybuild_validation.py).
4. Repeat the previous commands.



