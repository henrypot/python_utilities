
# JSON Structure Comparison Tool

This tool compares the structure of two JSON files and provides a detailed summary of the differences, including the count of nodes at each level and specific discrepancies between the two files.

## Features
- Parses and compares the structure of two JSON files.
- Identifies and logs detailed differences between the two JSON structures.
- Provides a summary of the total nodes at each level for both JSON files.
- Logs the comparison process and any errors encountered to a log file.

## Usage

### Command-Line Interface
You can run the script from the command line, providing the paths to the two JSON files you want to compare.

```sh
python compare_json_files.py <file1.json> <file2.json>
```

### Example
```sh
python compare_json_files.py file1.json file2.json
```

### Log File
The script generates a log file with the same name as the script, but with a `.log` extension. This log file contains all the details of the comparison process, including any errors encountered.

## Detailed Description of Functions

### json_comparison.py

#### parse_json_structure(json_data: Any) -> List[Tuple[int, int]]
Parses the JSON structure and counts nodes at each level.

#### compare_json_structures(json_data1: Any, json_data2: Any) -> Dict[str, Any]
Compares two JSON structures and finds detailed differences.

#### summarize_comparison(structure1: List[Tuple[int, int]], structure2: List[Tuple[int, int]], differences: Dict[str, Any]) -> Dict[str, Any]
Summarizes the comparison results, including total nodes at each level and detailed differences.

#### clean_and_unescape_json_string(json_str: str) -> str
Cleans and unescapes a JSON string.

#### read_json_from_file(file_path: str) -> Optional[Any]
Reads JSON from a file using ijson for streaming parsing.

#### print_comparison_summary(summary: Dict[str, Any]) -> None
Prints the comparison summary in a readable format.

### compare_json_files.py

#### main(file_path1: str, file_path2: str) -> None
Main function to execute the JSON comparison.

## Dependencies
- Python 3.x
- `ijson` library
- `logging` module (standard library)

## Installation

You can install the `ijson` library using pip:

```sh
pip install ijson
```


