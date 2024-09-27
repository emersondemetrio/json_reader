import os
import sys
import json
from typing import Any, Dict, List, Union, NewType

EXIT_CODES = ["0", "q", "Q"]
JSON_INDENTATION: int = 4

Path = NewType("Path", str)
JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JsonData = Dict[str, JsonValue]
JsonLike = Union[JsonData, List[Any]]
Flat = Dict[str, JsonValue]


def exit_if(condition: bool, message: str) -> None:
    if condition:
        print(message)
        sys.exit(1)


def get_data(file_name: str) -> JsonData:
    with open(file_name, "r") as file_content:
        return json.load(file_content)


def save_file(file_name: str, data: JsonData) -> None:
    with open(file_name, "w") as file_content:
        json.dump(data, file_content, indent=JSON_INDENTATION)


def flatten(data: JsonLike, prefix: str = "") -> Flat:
    result = {}
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{prefix}{key}" if prefix else key
            if isinstance(value, (dict, list)):
                result.update(flatten(value, f"{new_key}."))
            else:
                result[new_key] = value
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = f"{prefix}{i}"
            if isinstance(item, (dict, list)):
                result.update(flatten(item, f"{new_key}."))
            else:
                result[new_key] = item
    else:
        result[prefix.rstrip(".")] = data
    return result

def display_properties(data: Flat) -> None:
    properties = []

    for code, (path, value) in enumerate(data.items(), start=1):
        properties.append(f"Code: {code} | {path} = {value}")

    print("[Available properties]\n")
    print("\n".join(properties))
    print(f"\n\nEXIT = {', '.join(EXIT_CODES)}")

def request_input(data: Flat) -> str:
    display_properties(data)
    return input("\nEnter a code to edit: ")


def set_property(
    data: JsonData, property_path: List[str], value: JsonValue
) -> JsonData:
    if len(property_path) == 1:
        data[property_path[0]] = value
        return data

    key = property_path[0]  # ['prop1'] -> prop1
    if key not in data:
        data[key] = {}
    data[key] = set_property(data[key], property_path[1:], value)

    return data


def update(data: JsonData, property_path: Path, value: JsonValue) -> JsonData:
    return set_property(data, property_path.split("."), value)


def print_json(data: JsonData) -> None:
    print(json.dumps(data, indent=JSON_INDENTATION))


def main() -> None:
    exit_if(len(sys.argv) < 2, "Please provide a JSON file path as an argument.")
    file_path: str = sys.argv[1]
    exit_if(not os.path.exists(file_path), f"File {file_path} does not exist.")

    raw = get_data(file_path)

    while True:
        data = flatten(raw)
        prop = request_input(data)

        if prop in EXIT_CODES:
            print("Bye.")
            break

        try:
            prop = int(prop)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if prop < 1 or prop > len(data):
            print("Invalid code.")
            continue

        keys = list(data.keys())
        property_path = keys[prop - 1]

        new_value: str = input(
            f"Editing value for '{property_path}'\n\n"
            + "Value (press enter to finish): "
        )

        raw = update(raw, property_path, new_value)
        save_file(file_path, raw)
        print("JSON updated successfully.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")
        sys.exit(0)
