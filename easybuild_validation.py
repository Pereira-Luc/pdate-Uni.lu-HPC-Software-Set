import os
import glob
import sys
from typing import List, Tuple


# Path to the directory containing the log files
log_directory = ""


def check_installation_logs(directory: str) -> List[Tuple]:
    """
    Check all log files in the specified directory for key installation errors and collect brief summaries of relevant
    error messages.

    Args:
        directory (str): Path to the directory containing log files.

    Returns:
        List[Tuple]: List of tuples containing the module name, installation status, and brief error summaries (if any).
    """
    # Get a list of all .out log files in the specified directory
    log_files = glob.glob(os.path.join(directory, '*.out'))
    results = []

    # Define keywords and their short descriptions for identifying specific errors
    error_keywords = {
        "Checksum verification": "Checksum failure",
        "Sanity check failed:": "Sanity check failure",
        "make check": "Make check failure",
        "build failed": "Build Error"
    }

    for log_file in log_files:
        module_name = os.path.basename(log_file).rsplit('-', 1)[0]
        status = "valid"  # Assume the installation is valid unless an error is found
        error_summary = []  # Store summaries of specific error messages

        with open(log_file, 'r', encoding='utf-8') as file:
            for line in file:
                found_specific_error = False
                for key, summary in error_keywords.items():
                    if key in line:
                        print(f"Error in {module_name}: {line.strip()}")
                        status = "failed"
                        if summary not in error_summary:
                            error_summary.append(summary)
                        found_specific_error = True
                        break  # Stop checking after the first match

                if not found_specific_error and "error" in line.lower():
                    print(f"Error in {module_name}: {line.strip()}")
                    status = "failed"
                    if "Other installation error" not in error_summary:
                        error_summary.append("Other installation error")

        results.append((module_name, status, error_summary))

    # Sort results by module name
    results.sort(key=lambda x: x[0])

    return results


def report_results(results: List[Tuple]) -> None:
    """
    Print the results of the log file checks with colored output, including brief error summaries.

    Args:
        results (List[Tuple]): List of tuples containing module names, installation statuses, and error summaries.
    """
    # Iterate over the results which contain module name, status, and error summaries
    for module_name, status, error_summaries in results:
        # Check if the status is "valid" and print the module name in green text
        if status == "valid":
            print(f"{module_name}: \033[92m{status}\033[0m")

        # If the status is not "valid", print the module name in red text
        else:
            print(f"{module_name}: \033[91m{status}\033[0m")

            if error_summaries:
                for summary in error_summaries:
                    print(f"\033[91m Info: {summary}\033[0m")

        print()


if __name__ == '__main__':
    # Check if the first command-line argument is '-d' to set the log directory
    # Assign the log directory path from the second argument
    if sys.argv[1] is '-d':
        log_directory = sys.argv[2]

    # Check the logs for errors
    installation_results = check_installation_logs(log_directory)

    # Report the results
    report_results(installation_results)
