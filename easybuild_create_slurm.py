# Select "foss" to install foss toolchain 2023a
# Select "intel" to install foss toolchain 2023a
import sys


toolchain = "intel"

# Specify the number of CPU cores per job
job_cores = "8"

# Specify the max wall time in hours
max_walltime = "5"

# Set to True to use a dry run for debugging purposes
# Set to False to install modules
dry_run = False


def generate_slurm_script(eb_files, script_filename="test_install_modules.sh", dry_run=False):
    """
    Generates a Slurm script to load and install modules using EasyBuild with specified eb files,
    with an option for a dry run to simulate installations using GNU Parallel.

    Args:
        eb_files (list): List of full paths to EasyBuild (.eb) files.
        script_filename (str): Filename for the Slurm script.
        dry_run (bool): Whether to perform a dry run instead of a real installation.
    """
    if not eb_files:
        print("No EasyBuild files provided. Exiting...")
        return

    if len(eb_files) == 0:
        print("Error: No modules to install. Please check your file list.")
        return

    with open(script_filename, "w") as file:
        # Write the Slurm script header
        file.write("#!/bin/bash -l\n")
        file.write("#SBATCH --job-name=test-install-eb-modules\n")
        file.write("#SBATCH --output=out/test-install-eb-module-%j.out\n")
        file.write("#SBATCH --time=20:00:00\n")
        file.write("#SBATCH --partition=batch\n")
        file.write("#SBATCH --nodes=1\n")
        file.write("#SBATCH --mem=0\n")
        file.write("\n")

        # Function to print an error message and exit
        file.write("# Function to print an error message and exit\n")
        file.write("module purge\n")
        file.write("export EASYBUILD_JOB_BACKEND=Slurm\n")
        file.write("\n")
        
        file.write("print_error_and_exit() { echo \"***ERROR*** $*\"; exit 1; }\n")
        
         # Load the EasyBuild module
        file.write("# Load the EasyBuild module\n")
        file.write("module load tools/EasyBuild/4.9.1\n")
        file.write("\n")
        
        file.write("EBFILES=(" + ' '.join(f'"{file}"' for file in eb_files) + ")\n")
        file.write("mkdir -p logs\n")
        file.write("\n")

        command = "eb ${EBFILES[@]} --robot --job" if not dry_run else "eb ${EBFILES[@]} --robot -D"

        file.write(f"COMMAND='{command} --job-cores={job_cores} --job-max-walltime={max_walltime} --job-backend-config=slurm --trace --accept-eula-for=CUDA --accept-eula-for=Intel-oneAPI > logs/eb-log-{{#}}.log'\n")
        file.write("echo \"Running command: $COMMAND\"\n")
        file.write("\n")
        file.write("eval $COMMAND \n")
        
        file.write("\necho 'Tasks are all runing now sq to see them'\n")

    print(f"Slurm script generated: {script_filename}")


def read_eb_paths(file_path):
    """
    Reads EasyBuild configuration file paths from a text file.

    Args:
        file_path (str): Path to the text file containing EasyBuild file paths.

    Returns:
        list: A list of paths as strings.
    """
    with open(file_path, 'r') as file:
        paths = [line.strip() for line in file if line.strip()]
    return paths
    
if __name__ == "__main__":
    # Print a message indicating the start of the Slurm script creation process
    print("Creating associated Slurm script...")
    
    # first argument is the toolchain
    if len(sys.argv) > 1:
        toolchain = sys.argv[1]
            

    # Define input and script file names
    input_file = f"module_search_results_{toolchain}.txt"
    script_file = f"install_modules_{toolchain}.sh"

    # Read EasyBuild file paths
    eb_files = read_eb_paths(input_file)

    # Generate the Slurm script with the read EasyBuild files
    generate_slurm_script(eb_files, script_file, dry_run=dry_run)