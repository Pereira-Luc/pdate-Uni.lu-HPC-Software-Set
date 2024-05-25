def generate_slurm_script(eb_files, script_filename="test_install_modules.sh", dry_run=True):
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
        file.write("#!/bin/bash -l\n")
        file.write("#SBATCH --job-name=test-install-eb-modules\n")
        file.write("#SBATCH --output=test-install-eb-module-%j.out\n")
        file.write("#SBATCH --time=02:00:00\n")
        file.write("#SBATCH --partition=batch\n")
        file.write("#SBATCH --nodes=1\n")
        file.write("#SBATCH --exclusive\n")
        file.write("#SBATCH --mem=0\n")
        file.write("#SBATCH --ntasks-per-node=1\n")
        file.write("#SBATCH --cpus-per-task=4\n")
        file.write("\n")

        file.write("print_error_and_exit() { echo \"***ERROR*** $*\"; exit 1; }\n")
        file.write("hash parallel 2>/dev/null && test $? -eq 0 || print_error_and_exit \"Parallel is not installed on the system\"\n")
        file.write("\n")
        file.write("module load tools/EasyBuild/4.9.1\n")
        file.write("\n")
        file.write("EBFILES=(" + ' '.join(f'"{file}"' for file in eb_files) + ")\n")
        file.write("mkdir -p logs\n")
        file.write("\n")

        command = "eb {} --robot -D" if dry_run else "eb {} --robot -j $SLURM_CPUS_PER_TASK"
        srun_command = "srun --exclusive -n1 -c $SLURM_CPUS_PER_TASK --cpu-bind=cores"
        verbose_flag = "--verbose"

        file.write(f"parallel --delay 0.2 -j ${{SLURM_NTASKS_PER_NODE}} {verbose_flag} --joblog eb-joblog.log ")
        file.write(f"\"{srun_command} {command} > logs/eb-log-{{#}}.log\" ::: \"${{EBFILES[@]}}\"\n")
        file.write("\necho 'EasyBuild installations completed'\n")

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
    print("Running as a standalone script...")
    # Example usage
    #eb_files = read_eb_paths("module_search_results.txt")
    eb_files = read_eb_paths("all_module_search_results3Back.txt")
    generate_slurm_script(eb_files)