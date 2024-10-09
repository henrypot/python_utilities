import json
import ijson
import logging
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Optional

def parse_json_structure(json_data: Any) -> List[Tuple[int, int]]:
    """
    Parse the JSON structure and count nodes at each level.
    
    Args:
    json_data (Any): The JSON data to parse.

    Returns:
    List[Tuple[int, int]]: A list of tuples where each tuple contains the level and the count of nodes at that level.
    """
    levels = defaultdict(int)

    def traverse(node: Any, level: int = 1) -> None:
        """Recursively traverse the JSON structure and count nodes."""
        if isinstance(node, dict):
            levels[level] += 1
            for key in node:
                traverse(node[key], level + 1)
        elif isinstance(node, list):
            levels[level] += 1
            for item in node:
                traverse(item, level + 1)
        else:
            levels[level] += 1

    traverse(json_data)
    return sorted(levels.items())


def compare_json_structures(json_data1: Any, json_data2: Any) -> Dict[str, Any]:
    """
    Compare two JSON structures and find detailed differences.
    
    Args:
    json_data1 (Any): The first JSON structure.
    json_data2 (Any): The second JSON structure.

    Returns:
    Dict[str, Any]: A dictionary containing the differences between the two JSON structures.
    """
    detailed_differences = {}

    def find_differences(d1: Any, d2: Any, path: str = '') -> None:
        """Recursively find differences between two JSON structures."""
        if isinstance(d1, dict) and isinstance(d2, dict):
            keys = set(d1.keys()).union(d2.keys())
            for key in keys:
                new_path = f'{path}/{key}' if path else key
                if key in d1 and key in d2:
                    find_differences(d1[key], d2[key], new_path)
                elif key in d1:
                    detailed_differences[new_path] = {'body1': d1[key], 'body2': 'Key not found'}
                else:
                    detailed_differences[new_path] = {'body1': 'Key not found', 'body2': d2[key]}
        elif isinstance(d1, list) and isinstance(d2, list):
            len1, len2 = len(d1), len(d2)
            for index in range(max(len1, len2)):
                new_path = f'{path}[{index}]'
                if index < len1 and index < len2:
                    find_differences(d1[index], d2[index], new_path)
                elif index < len1:
                    detailed_differences[new_path] = {'body1': d1[index], 'body2': 'Element not found'}
                else:
                    detailed_differences[new_path] = {'body1': 'Element not found', 'body2': d2[index]}
        elif d1 != d2:
            detailed_differences[path] = {'body1': d1, 'body2': d2}

    find_differences(d1=json_data1, d2=json_data2)
    return detailed_differences


def summarize_comparison(structure1: List[Tuple[int, int]], structure2: List[Tuple[int, int]], differences: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarize the comparison results.
    
    Args:
    structure1 (List[Tuple[int, int]]): The structure of the first JSON data.
    structure2 (List[Tuple[int, int]]): The structure of the second JSON data.
    differences (Dict[str, Any]): The detailed differences between the two JSON structures.

    Returns:
    Dict[str, Any]: A summary of the comparison results.
    """
    total_nodes1 = sum(count for _, count in structure1)
    total_nodes2 = sum(count for _, count in structure2)

    summary = {
        "total_nodes": {
            "body1": total_nodes1,
            "body2": total_nodes2
        },
        "detailed_comparison": [],
        "differences": differences
    }

    max_level = max(max(level for level, _ in structure1), max(level for level, _ in structure2))

    for level in range(1, max_level + 1):
        count1 = next((count for l, count in structure1 if l == level), 0)
        count2 = next((count for l, count in structure2 if l == level), 0)
        summary["detailed_comparison"].append({
            "level": level,
            "body1": count1,
            "body2": count2,
            "difference": count1 - count2
        })

    return summary


def clean_and_unescape_json_string(json_str: str) -> str:
    """
    Clean and unescape a JSON string.
    
    Args:
    json_str (str): The JSON string to clean and unescape.

    Returns:
    str: The cleaned and unescaped JSON string.
    """
    try:
        # Use ast.literal_eval to unescape the JSON string
        return ast.literal_eval(f'"{json_str}"')
    except (ValueError, SyntaxError) as e:
        logging.error(f"Error unescaping JSON string: {e}")
        return json_str


def read_json_from_file(file_path: str) -> Optional[Any]:
    """
    Read JSON from a file using ijson for streaming parsing.
    
    Args:
    file_path (str): The path to the JSON file.

    Returns:
    Optional[Any]: The parsed JSON data, or None if an error occurred.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Stream and parse the JSON content
            json_data = ijson.items(file, '')
            for item in json_data:
                return item
    except FileNotFoundError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None
    except IOError as e:
        logging.error(f"IO error reading file {file_path}: {e}")
        return None


def print_comparison_summary(summary: Dict[str, Any]) -> None:
    """
    Print the comparison summary in a readable format.
    
    Args:
    summary (Dict[str, Any]): The comparison summary to print.
    """
    logging.info("Comparison Summary:")
    logging.info(f"Total Nodes: body1 = {summary['total_nodes']['body1']}, body2 = {summary['total_nodes']['body2']}\n")
    logging.info("Detailed Comparison:")
    for detail in summary["detailed_comparison"]:
        logging.info(f"Level {detail['level']}: body1 = {detail['body1']}, body2 = {detail['body2']}, difference = {detail['difference']}")
    if summary["differences"]:
        logging.info("\nDifferences:")
        for path, diff in summary["differences"].items():
            logging.info(f"Path: {path}")
            logging.info(f"  body1: {diff['body1']}")
            logging.info(f"  body2: {diff['body2']}\n")
