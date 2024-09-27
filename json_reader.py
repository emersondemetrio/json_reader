import os
import sys
import json
from typing import Any, Dict, List, Union, TypedDict, NewType

EXIT_CODES = [0, "q", "Q"]
JSON_INDENTATION: int = 4

Path = NewType("Path", str)
JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JsonData = Dict[str, JsonValue]
JsonLike = Union[JsonData, List[Any]]


class KeyValuePair(TypedDict):
    path: Path
    value: JsonValue


KeyValueMap = List[KeyValuePair]


def exit_if(condition: bool, message: str) -> None:
    if not condition:
        return

    print(message)
    sys.exit(1)


def get_json_data(file_name: str) -> JsonData:
    with open(file_name, "r") as file_content:
        return json.load(file_content)


def save_json_file(file_name: str, data: JsonData) -> None:
    with open(file_name, "w") as file_content:
        json.dump(data, file_content, indent=JSON_INDENTATION)


def key_exists(kv_map: KeyValueMap, prop: int) -> bool:
    return prop - 1 in range(len(kv_map))


def get_key_value_property_map(
    path: Path, json_data: JsonLike, ref: KeyValueMap = []
) -> KeyValueMap:
    for key_name, value in json_data.items():
        if isinstance(key_name, list):
            for i, item in enumerate(value):
                get_key_value_property_map(
                    (path + "." if path != "" else "") + key_name + " " + str(i), item
                )
        elif isinstance(value, dict):
            get_key_value_property_map(
                (path + "." if path != "" else "") + key_name, value
            )
        else:
            cur_path = path + "." + key_name if path != "" else key_name
            ref.append({"path": cur_path, "value": value})
    return ref


def show_json_properties(kv_map: KeyValueMap) -> str:
    print("\n[Available properties] \n")

    for idx, act in enumerate(kv_map, start=1):
        print(f"Code: {idx}\t | {act['path']} = {act['value']}")

    print("\nEXIT = 0")

    return input("\nEnter a code to edit: ")


def update_json_property(
    data: JsonData, property_path: List[str], value: JsonValue
) -> JsonData:
    if len(property_path) == 1:
        key = property_path[0] # ['outer_1'] -> 'outer_1'
        data[key] = value

        return data

    return update_json_property(data[property_path[0]], property_path[1:], value)


def update_json(data: JsonData, property_path: Path, value: JsonValue) -> JsonData:
    updated = update_json_property(data, property_path.split("."), value)
    print("updated", updated)

    return updated

def print_json(data: JsonData) -> None:
    print(json.dumps(data, indent=JSON_INDENTATION))

def main() -> None:
    file_path: str = sys.argv[1]
    exit_if(not os.path.exists(file_path), f"File {file_path} does not exist.")

    json_data: JsonData = get_json_data(file_path)

    while True:
        kv_map = get_key_value_property_map(Path(""), json_data)

        prop = show_json_properties(kv_map)

        exit_if(prop in EXIT_CODES, "Bye.")

        prop = int(prop)
        exit_if(not key_exists(kv_map, prop), "Invalid code.")

        property_path: Path = kv_map[prop - 1]["path"]
        new_value: str = input(
            f"Editing value for '{property_path}'\n\n"
            + "Value (press enter to finish): "
        )

        json_data = update_json(json_data, property_path, new_value)
        save_json_file(file_path, json_data)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
        print("\nBye.")
