import os
import glob
import sys

def check_installation_logs(directory):
    """
    Check all log files in the specified directory for key installation errors and collect brief summaries of relevant error messages.

    Args:
        directory (str): Path to the directory containing log files.

    Returns:
        list: List of tuples containing the module name, installation status, and brief error summaries (if any).
    """
    log_files = glob.glob(os.path.join(directory, '*.out'))
    results = []

    # Define keywords and their short descriptions
    error_keywords = {
        "Checksum verification": "Checksum failure",
        "Sanity check failed:": "Sanity check failure",
        "make check": "Make check failure"
    }

    for log_file in log_files:
        module_name = os.path.basename(log_file).rsplit('-', 1)[0]
        status = "valid"  # Assume the installation is valid unless an error is found
        error_summary = []  # Store summaries of specific error messages

        with open(log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            found_specific_error = False

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

        results.append((module_name, status, error_summary))

    # Sort results by module name
    results.sort(key=lambda x: x[0])

    return results

def report_results(results):
    """
    Print the results of the log file checks with colored output, including brief error summaries.

    Args:
        results (list): List of tuples containing module names, installation statuses, and error summaries.
    """
    for module_name, status, error_summaries in results:
        if status == "valid":
            print(f"{module_name}: \033[92m{status}\033[0m")  # Green text
        else:
            print(f"{module_name}: \033[91m{status}\033[0m")  # Red text
            if error_summaries:
                for summary in error_summaries:
                    print(f"\033[91m Info: {summary}\033[0m")  # Print each summary in red
            print()  # Print a newline for better separation

if __name__ == '__main__':
    # Path to the directory containing the log files
    log_directory = './'
    
    if (sys.argv[1] == '-d'):
        log_directory = sys.argv[2]

    # Check the logs for errors
    installation_results = check_installation_logs(log_directory)

    # Report the results
    report_results(installation_results)
