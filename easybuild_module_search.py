import subprocess
from typing import TextIO, List


# Select "foss" to install foss toolchain 2023a
# Select "intel" to install foss toolchain 2023a
toolchain = "foss"

# Set to True to create a file with the installation paths only
# Set to False to get all the dependencies and count them
create_install_file = True


def search_modules(modules: List[str],
                   grep_filter: str = None,
                   output_file="module_search_results.txt"):
    """
    Searches for specified modules using EasyBuild, optionally filters the output,
    and saves the results to a file.

    Args:
    modules (List[str]): List of module names to search for.
    toolchain (str): Toolchain version to use in the search.
    grep_filter (str, optional): Filter term to use with grep. Defaults to None.
    output_file (str): Filename to save the output results.
    """
    # Initialize a list to hold dependencies for all modules
    global_dependency_list = []

    # Open the output file for writing
    with open(output_file, "w") as file:
        for module in modules:
            print("==================================================")
            print(f"Searching for {module}...")

            # Construct the command to search for the module with EasyBuild
            command = f"eb --search '{module}.*'"

            # If a grep filter is specified, add it to the command
            if grep_filter:
                command += f" | grep '{grep_filter}'"
            
            # Execute the command
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Write the results to file
            if not create_install_file:
                file.write(f"Search results for {module}:")
                file.write(stdout.decode())
            
            # Convert stdout to a list of lines
            lines = stdout.decode().split("\n")
            if lines[-1] == '':
                lines = lines[:-1]

            # If no versions of the module are found
            if len(lines) == 0:
                print(f"No versions of {module} found.")

                if not create_install_file:
                    file.write("No versions found.\n")
                    file.write("\n" + "-"*40 + "\n")

                print("==================================================\n")

                continue

            # By default, select the first module found
            selected_module = lines[0]

            # If more than one version is found, let the user choose
            if len(lines) > 1:
                print(f"Found {len(lines)} versions of {module}.\n")

                selected_module = ask_user_which_module(lines, path_filter=module)

                if selected_module is None:
                    print("No module selected.")
                    print("==================================================\n")

                    continue

            # Extract the module name from the selected line
            selected_module = selected_module.split(" ")[-1]
            file.write(selected_module+"\n")
            print(f"\nSelected module: {selected_module}")

            # Print errors if found
            if stderr:
                print("Errors found.")

                if not create_install_file:
                    file.write("Errors:\n")
                    file.write(selected_module)

            # List dependencies for each found module
            if not create_install_file:
                dependencies = list_dependencies(selected_module, file)
                global_dependency_list.extend(dependencies)

            print("==================================================\n")

        # Find unique dependencies from the global list and return them
        if not create_install_file:    
            unique_dependencies = set(global_dependency_list)
            print(f"Total unique dependencies found: {len(unique_dependencies)}")

            return unique_dependencies


def ask_user_which_module(list_of_modules: List[str],
                          path_filter: str = None) -> str:
    """
    Ask the user to choose a module from a list of modules.

    Args:
        list_of_modules (List[str]): List of module names to choose from.
        path_filter (str, optional): Optional filter term to refine the module paths. Defaults to None.

    Returns:
        str: The selected module path.
    """
    while True:

        print("Please select a module: ")

        # Display the list of modules for the user to choose from
        for i, module in enumerate(list_of_modules):
            # If a path filter is specified, modify the module path accordingly
            if path_filter:
                module = module.split(path_filter)[-1]
                module = path_filter + module
            
            print(f"{i+1}. {module}")

        # Prompt the user to enter their choice
        choice = input("Enter the number of the module or 0 for none: ")

        try:
            choice = int(choice)

            # If the user chooses 0, exit the function
            if choice == 0:
                print("Exiting...")
                return None

            # Check if the choice is within the valid range
            if choice < 1 or choice > len(list_of_modules):
                print("Invalid choice. Please try again.")
                continue

        # Handle invalid choice
        except ValueError:
            print("Invalid choice. Please try again.")
            continue

        # Return the selected module path
        return list_of_modules[choice - 1]
            

def list_dependencies(module: str,
                      file: TextIO) -> List[str]:
    """
    List dependencies of found modules using EasyBuild's dry-run option.

    Args:
    module (str): Module name to list dependencies for.
    file (TextIO): File object to write dependencies to.

    Returns:
    List[str]: List of dependencies for the module.
    """
    print(f"Listing dependencies for {module}...")

    # Construct the command to list dependencies with EasyBuild's dry-run option
    command = f"eb '{module}' -D"

    # Execute the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # If errors occur during the listing process, write them to the file and return an empty list
    if stderr:
        if not create_install_file:
            file.write("Errors in dependencies listing:\n")
            file.write(stderr.decode())

        return []

    # Extracting dependencies
    dependencies = []

    # Write dependency details to the file for dry-run
    if not create_install_file:
        file.write(f"Dependency details for {module}:\n")

    # Iterate through each line of the stdout and extract dependencies
    for line in stdout.decode().split('\n'):
        if line.strip().startswith('*'):
            dependency = line.split('(')[1].split(')')[0]
            dependencies.append(dependency)

    # Write dependency details to the file for dry-run
    if not create_install_file:          
        file.write("\n".join(dependencies))    
    
    return dependencies


def list_all_modules() -> List[str]:
    """
    Uses the 'module avail' command to list all available modules and extracts their names.

    Returns:
    List[str]: A list containing the names of all modules available.
    """
    try:
        # Execute the 'module avail' command
        command = "module avail"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        print("Getting all modules...")

        # Combine stdout and stderr into a single string
        output = stdout.decode() + stderr.decode()

        # Initialize a list to store module names
        module_names = []

        # Process each line in the output
        for line in output.split('\n'):
            # Check if the line is not empty and contains a '/'
            if line.strip() and '/' in line:
                parts = line.split('/')

                # Assuming the 'module' is the second segment in the path 'smth/module/...'
                if len(parts) > 1:
                    module_name = parts[1]  # Get the module name which is the second part of the path
                    module_names.append(module_name)

        # Remove duplicates by converting to a set and back to a list
        module_list = list(set(module_names))
        print(f"Total modules found: {len(module_list)}")
        return module_list

    # Handle any errors that occur during the process
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


if __name__ == "__main__":
    # List of modules to search for
    modules = ["GROMACS", "ABAQUS", "OpenFOAM",
               "ParaView", "gnuplot",
               "Julia", "Rust", "Python",
               "TensorFlow", "PyTorch", "PyTorch-Lightning", "Spark",
               "Armadillo", "GDAL", "GSL", "Eigen"]

    # Grep filter to use for filtering search results
    grep_filter = f"{toolchain}-2023a"

    # Output file to save search results
    output_file = f"module_search_results_{toolchain}.txt"

    # Get a list of all available modules
    all_modules = list_all_modules()

    # Search for the specified modules using grep filter and save results to the output file
    search_modules(all_modules, grep_filter, output_file)

    print(f"Search completed. Results are saved in {output_file}.")
