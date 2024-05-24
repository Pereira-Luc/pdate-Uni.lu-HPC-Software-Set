
def generate_slurm_script(eb_files, script_filename="test_install_modules.sh", dry_run=True):
    """
    Generates a Slurm script to load and install modules using EasyBuild with specified eb files,
    with an option for a dry run to simulate installations.

    Args:
        eb_files (list): List of full paths to EasyBuild (.eb) files.
        script_filename (str): Filename for the Slurm script.
        dry_run (bool): Whether to perform a dry run instead of a real installation.
    """
    if not eb_files:
        print("No EasyBuild files provided. Exiting...")
        return

    num_files = len(eb_files)
    if num_files == 0:
        print("Error: No modules to install. Please check your file list.")
        return
    
    with open(script_filename, "w") as file:
        file.write("#!/bin/bash\n")
        file.write("#SBATCH --job-name=test-install-eb-modules\n")
        file.write(f"#SBATCH --array=0-{num_files-1}\n")  # Limits the number of concurrent jobs to 10; adjust as needed
        file.write("#SBATCH --output=test-install-eb-module-%A_%a.out\n")
        file.write("#SBATCH --time=02:00:00\n")
        file.write("#SBATCH --ntasks=1\n")
        file.write("#SBATCH --cpus-per-task=4\n")  # Adjust the number of CPUs per task
        file.write("#SBATCH --mem=4G\n")  # Adjust memory per task
        file.write("\n")

        file.write("module load EasyBuild\n")  # Adjust if your module load command differs
        file.write("EBFILES=({})\n".format(' '.join(f'"{file}"' for file in eb_files)))

        if dry_run:
            file.write("eb ${EBFILES[$SLURM_ARRAY_TASK_ID-1]} --robot -D\n")
        else:
            file.write("eb ${EBFILES[$SLURM_ARRAY_TASK_ID-1]} --robot -j $SLURM_CPUS_PER_TASK\n")

        file.write("\necho 'Dry run completed for module $SLURM_ARRAY_TASK_ID'\n")

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
    # Example usage
    #eb_files = read_eb_paths("module_search_results.txt")
    eb_files = read_eb_paths("all_module_search_results3Back.txt")
    generate_slurm_script(eb_files)