import subprocess


create_install_file = False # Set to True to create a file with the installation paths only false to get all the dependencies and count them


def search_modules(modules, grep_filter=None, output_file="module_search_results.txt"):
    """
    Searches for specified modules using EasyBuild, optionally filters the output,
    and saves the results to a file.

    Args:
    modules (list): List of module names to search for.
    toolchain (str): Toolchain version to use in the search.
    grep_filter (str, optional): Filter term to use with grep. Defaults to None.
    output_file (str): Filename to save the output results.
    """
    global_dependency_list = []
    
    with open(output_file, "w") as file:
        for module in modules:
            print("=====================================")
            print(f"Searching for {module}...")
            command = f"eb --search '{module}-*'"
            
            # print(f"Executing command: {command}")
            if grep_filter:
                command += f" | grep '{grep_filter}'"
                # print(f"Filtering results with: {grep_filter}")
            
            # Execute the command
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Write the results to file
            if not create_install_file:
                file.write(f"Search results for {module}:\n")
                file.write(stdout.decode())
            
            # convert stdout to a list of lines
            lines = stdout.decode().split("\n")
            print(f"Found {len(lines) - 1} versions of {module}.")
            
            if (len(lines) - 1)  == 0:
                print(f"No versions of {module} found.")
                if not create_install_file:
                    file.write("No versions found.\n")
                    file.write("\n" + "-"*40 + "\n")
                print("=====================================")
                print()
                continue
        
            selected_module = lines[0]
            
            if len(lines) > 2:
                print(f"Found {len(lines) - 1} versions of {module}.")
                # Ask the user to choose a module
                selected_module = ask_user_which_module(lines, path_filter=module)
                if selected_module is None:
                    print("No module selected")
                    print("=====================================")
                    print()
                    continue
            
            selected_module = selected_module.split(" ")[-1]
            file.write(selected_module+"\n")
            
            print(f"Selected module: {selected_module}")
            
            if stderr:
                print("Errors found:")
                if not create_install_file:
                    file.write("Errors:\n")
                    file.write(selected_module)
            
            # List dependencies for each found module
            if not create_install_file:
                dependencies = list_dependencies(selected_module, file)
                global_dependency_list.extend(dependencies)
            print("=====================================")
            print()
            
            
            #file.write("\n" + "-"*40 + "\n")
        if not create_install_file:    
            unique_dependencies = set(global_dependency_list)  # Set to find unique elements
            print(f"Total unique dependencies found: {len(unique_dependencies)}")
            return unique_dependencies

            
def ask_user_which_module(list_of_modules, path_filter=None):
    """
    Ask the user to choose a module from a list of modules.
    
    Args:
        list_of_modules (list): List of module names to choose from.
    
    Returns:
        str: The selected module path
    """
    
    while True:
        print("Please select a module:")
        for i, module in enumerate(list_of_modules):
            
            if path_filter:
                module = module.split(path_filter)[-1]
                module = path_filter + module
            
            print(f"{i+1}. {module}")
        
        choice = input("Enter the number of the module 0 for none: ")
        try:
            choice = int(choice)
            
            if choice == 0:
                print("Exiting...")
                return None
            
            if choice < 1 or choice > len(list_of_modules):
                print("Invalid choice. Please try again.")
                continue
        except ValueError:
            print("Invalid choice. Please try again.")
            continue
        
        return list_of_modules[choice - 1]
            

def list_dependencies(module, file):
    """
    List dependencies of found modules using EasyBuild's dry-run option.

    Args:
    module (str): Module name to list dependencies for.
    file (file object): File object to write dependencies to.

    Returns:
    list: List of dependencies for the module.
    """
    print(f"Listing dependencies for {module}...")
    command = f"eb '{module}' -D"  # Ensure using dry-run option

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        if not create_install_file:
            file.write("Errors in dependencies listing:\n")
            file.write(stderr.decode())
        return []

    # Extracting dependencies
    dependencies = []
    if not create_install_file:
        file.write(f"Dependency details for {module}:\n")

    for line in stdout.decode().split('\n'):
        if line.strip().startswith('*'):
            # dependancy name is inside the ()
            dependencie = line.split('(')[1].split(')')[0]
            dependencies.append(dependencie)
         
    if not create_install_file:          
        file.write("\n".join(dependencies))    
    
    return dependencies

def list_all_modules():
    """
    Uses the 'module avail' command to list all available modules and extracts their names.

    Returns:
    list: A list containing the names of all modules available.
    """
    try:
        # Execute the 'module avail' command
        command = "module avail"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        print("Getting all modules...")

        output = stdout.decode() + stderr.decode()
        # Initialize a list to store module names
        module_names = []

        # Process each line in the output
        for line in output.split('\n'):
            if line.strip() and '/' in line:
                parts = line.split('/')
                # Assuming the 'module' is the second segment in the path 'smth/module/...'
                if len(parts) > 1:
                    module_name = parts[1]  # Get the module name which is the second part of the path
                    module_names.append(module_name)

        module_list = list(set(module_names))
        print(f"Total modules found: {len(module_list)}")
        return module_list 

    except Exception as e:
        print(f"An error occurred: {e}")
        return []


if __name__ == "__main__":
    modules = ["GROMACS", "ABAQUS", "OpenFOAM","ParaView","gnuplot", "Julia", "Rust", "Python", "TensorFlow", "PyTorch", "PyTorch-Lightning", "Spark", "Armadillo", "GDAL","GSL", "Eigen"]
    grep_filter = "foss-2023a" 
    output_file = "module_search_results.txt"
    #search_modules(modules, grep_filter, output_file=output_file)
    #print(f"Search completed. Results are saved in {output_file}.")
    
    all_modules = list_all_modules()
    
    search_modules(all_modules, grep_filter, output_file="all_module_search_results3.txt")
    print(f"Search completed. Results are saved in all_module_search_results2.txt.")
    
    
    # First pass with big software list now we can get all ther rest of the dependencies with mdoule avail command
    
