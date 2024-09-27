import os
import sys
import json
from typing import Any, Dict, List, Union, NewType

EXIT_CODES = [0, "q", "Q"]
JSON_INDENTATION: int = 4

Path = NewType("Path", str)
JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JsonData = Dict[str, JsonValue]
JsonLike = Union[JsonData, List[Any]]


def exit_if(condition: bool, message: str) -> None:
    if condition:
        print(message)
        sys.exit(1)


def get_json_data(file_name: str) -> JsonData:
    with open(file_name, "r") as file_content:
        return json.load(file_content)


def save_json_file(file_name: str, data: JsonData) -> None:
    with open(file_name, "w") as file_content:
        json.dump(data, file_content, indent=JSON_INDENTATION)


def flatten_json(data: JsonLike, prefix: str = "") -> Dict[str, JsonValue]:
    result = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{prefix}{key}" if prefix else key
            if isinstance(value, (dict, list)):
                result.update(flatten_json(value, f"{new_key}."))
            else:
                result[new_key] = value
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = f"{prefix}{i}"
            if isinstance(item, (dict, list)):
                result.update(flatten_json(item, f"{new_key}."))
            else:
                result[new_key] = item
    else:
        result[prefix.rstrip(".")] = data
    return result


def show_json_properties(flattened: Dict[str, JsonValue]) -> str:
    print("\n[Available properties] \n")
    for idx, (path, value) in enumerate(flattened.items(), start=1):
        print(f"Code: {idx}\t | {path} = {value}")
    print("\nEXIT = 0")
    return input("\nEnter a code to edit: ")


def update_json_property(
    data: JsonData, property_path: List[str], value: JsonValue
) -> JsonData:
    if len(property_path) == 1:
        data[property_path[0]] = value
        return data
    key = property_path[0]
    if key not in data:
        data[key] = {}
    data[key] = update_json_property(data[key], property_path[1:], value)
    return data


def update_json(data: JsonData, property_path: Path, value: JsonValue) -> JsonData:
    return update_json_property(data, property_path.split("."), value)


def print_json(data: JsonData) -> None:
    print(json.dumps(data, indent=JSON_INDENTATION))


def main() -> None:
    exit_if(len(sys.argv) < 2, "Please provide a JSON file path as an argument.")
    file_path: str = sys.argv[1]
    exit_if(not os.path.exists(file_path), f"File {file_path} does not exist.")

    json_data: JsonData = get_json_data(file_path)

    while True:
        flattened = flatten_json(json_data)
        prop = show_json_properties(flattened)

        if prop in EXIT_CODES:
            print("Bye.")
            break

        try:
            prop = int(prop)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if prop < 1 or prop > len(flattened):
            print("Invalid code.")
            continue

        property_path = list(flattened.keys())[prop - 1]
        new_value: str = input(
            f"Editing value for '{property_path}'\n\n"
            + "Value (press enter to finish): "
        )

        json_data = update_json(json_data, property_path, new_value)
        save_json_file(file_path, json_data)
        print("JSON updated successfully.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")
        sys.exit(0)
