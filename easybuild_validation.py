import os
import glob
import sys
from typing import List, Tuple


# Path to the directory containing the log files
log_directory = "./eb_logs_intel"


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
        "make check": "Make check failure"
    }

    # Iterate over each log file to analyze its content
    for log_file in log_files:
        # Extract the module name from the log file name
        module_name = os.path.basename(log_file).rsplit('-', 1)[0]

        # Assume the installation is valid unless an error is found
        status = "valid"

        # Store summaries of specific error messages
        error_summary = []

        # Open the log file and read its lines
        with open(log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            # Flag to check if a specific error keyword was found
            found_specific_error = False

            # Check each line in the log file for error keywords
            for line in lines:
                for key, summary in error_keywords.items():
                    if key in line:
                        status = "failed"
                        if summary not in error_summary:
                            error_summary.append(summary)
                        found_specific_error = True

            # Append a general error summary if no specific keywords were found in any error line
            if status == "failed" and not found_specific_error:
                error_summary.append("Other installation error")

        # Append the results for the current log file (module name, status, error summaries)
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
