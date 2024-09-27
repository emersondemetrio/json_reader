import os
import sys
import json
from typing import Any, Dict, List, Union, TypedDict, NewType

EXIT_CODE: int = 0

Path = NewType('Path', str)
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


def update_json_kv_data(path: Path, json_data: JsonLike, ref: KeyValueMap = []) -> KeyValueMap:
    if isinstance(json_data, dict):
        for key_name, value in json_data.items():
            if isinstance(value, list):
                for i, item in enumerate(value):
                    new_path = Path((path + "." if path != "" else "") + key_name + " " + str(i))
                    update_json_kv_data(new_path, item, ref)
            elif isinstance(value, dict):
                new_path = Path((path + "." if path != "" else "") + key_name)
                update_json_kv_data(new_path, value, ref)
            else:
                ref.append(KeyValuePair(
                    path=Path((path + "." + key_name if path != "" else key_name)),
                    value=value
                ))
    elif isinstance(json_data, list):
        for i, item in enumerate(json_data):
            new_path = Path((path + " " if path != "" else "") + str(i))
            update_json_kv_data(new_path, item, ref)

    return ref


def show_json_properties(key_value_map: KeyValueMap) -> int:
    print("Available properties are: \n")

    for idx, act in enumerate(key_value_map, start=1):
        print(f"Code: {idx}\t| Property: {act['path']} = {act['value']}")

    print("\nEXIT", "Code:", 0)

    return int(
        input(
            "\nEnter a code to edit: ",
        )
    )


def read_json_file(file_name: str) -> JsonData:
    with open(file_name, "r") as file_content:
        return json.load(file_content)


def update_json_data(json_data: JsonData, path: List[str], value: JsonValue) -> JsonData:
    if len(path) == 1:
        json_data[path[0]] = value
        return json_data

    return update_json_data(json_data[path[0]], path[1:], value)


def update_json_property(json_data: JsonData, property_path: Path, v: JsonValue) -> str:
    updated = update_json_data(json_data, property_path.split("."), v)

    return json.dumps(updated, indent=4, sort_keys=True)


def main() -> None:
    file_path: str = sys.argv[1]
    exit_if(not os.path.exists(file_path), f"File {file_path} does not exist.")

    json_data: JsonData = read_json_file(file_path)

    while True:
        kv_map: KeyValueMap = update_json_kv_data(Path(""), json_data)
        prop: int = show_json_properties(kv_map)

        exit_if(prop == EXIT_CODE, "Bye.")

        property_path: Path = kv_map[prop - 1]["path"]
        new_value: str = input(
            f"Editing value for '{property_path}'\n\n"
            + "Value (press enter to finish): "
        )

        json_data = json.loads(update_json_property(json_data, property_path, new_value))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")