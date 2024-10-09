import sys
import time
import logging
from json_comparison import (
    read_json_from_file,
    parse_json_structure,
    compare_json_structures,
    summarize_comparison,
    print_comparison_summary
)

# Set up logging
script_name = "compare_json_files"
log_filename = f"{script_name}.log"
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler(log_filename),
    logging.StreamHandler()
])

def main(file_path1: str, file_path2: str) -> None:
    """
    Main function to execute the JSON comparison.
    
    Args:
    file_path1 (str): The path to the first JSON file.
    file_path2 (str): The path to the second JSON file.
    """
    start_time = time.time()  # Start timing

    read_start_time = time.time()
    json_data1 = read_json_from_file(file_path1)
    json_data2 = read_json_from_file(file_path2)
    read_end_time = time.time()

    if json_data1 and json_data2:
        parse_start_time = time.time()
        structure1 = parse_json_structure(json_data1)
        structure2 = parse_json_structure(json_data2)
        parse_end_time = time.time()

        compare_start_time = time.time()
        differences = compare_json_structures(json_data1, json_data2)
        compare_end_time = time.time()

        summarize_start_time = time.time()
        summary = summarize_comparison(structure1, structure2, differences)
        summarize_end_time = time.time()

        if summary:
            print_comparison_summary(summary)
        else:
            logging.error("Comparison could not be completed due to errors in the JSON structures.")
    else:
        logging.error("One or both JSON files could not be read.")

    end_time = time.time()  # End timing
    duration = end_time - start_time

    logging.info(f"\nTiming Details:")
    logging.info(f"  Reading JSON files: {read_end_time - read_start_time:.2f} seconds")
    logging.info(f"  Parsing JSON structures: {parse_end_time - parse_start_time:.2f} seconds")
    logging.info(f"  Comparing JSON structures: {compare_end_time - compare_start_time:.2f} seconds")
    logging.info(f"  Summarizing comparison: {summarize_end_time - summarize_start_time:.2f} seconds")
    logging.info(f"Total duration: {duration:.2f} seconds")


# Example usage with file names as input parameters
if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python compare_json_files.py <file1.json> <file2.json>")
    else:
        file_path1 = sys.argv[1]
        file_path2 = sys.argv[2]
        main(file_path1, file_path2)
