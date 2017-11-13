#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JSON reader
"""

from __future__ import print_function
import os
import sys
import shutil
import json

"""
with open("replayScript.json", "r") as jsonFile:
    data = json.load(jsonFile)

tmp = data["location"]
data["location"] = "NewPath"

with open("replayScript.json", "w") as jsonFile:
    json.dump(data, jsonFile)
"""

ENV_LIST = [
    {
        "name": "development",
        "code": 1,
        "filename": "development.json"
    }, {
        "name": "docker",
        "code": 2,
        "filename": "docker.json"
    }, {
        "name": "testing",
        "code": 3,
        "filename": "testing.json"
    }
]

ACTIONS = []

def get_info(header, msg):
    """Read info"""

    print(header)
    return raw_input(msg)

def get_json_keys(path, json_data):
    """
    Show all json keys
    """

    for key_name, value in json_data.iteritems():

        if isinstance(key_name, list):
            for i, item in enumerate(value):
                get_json_keys(
                    (path + "." if path != "" else "") + key_name + " " + str(i),
                    item
                )
        elif isinstance(value, dict):
            get_json_keys(
                (path + "." if path != "" else "") + key_name,
                value
            )
        else:
            cur_path = (path + "." + key_name if path != "" else key_name)
            #output = "{}: '{}'".format(cur_path, value)
            ACTIONS.append({
                "path": cur_path,
                "value": value
            })

def show_avaliable_options(json_data):
    """
    COMO
    """

    get_json_keys("", json_data)

    print("Avaliable Options are: \n")

    for idx, act in enumerate(ACTIONS, start=1):
        print("Code:", idx, "\tACTION", act["path"])

    print("\nEXIT", "Code:", 0)

    return int(
        get_info("\nChoose one code to edit.", "Code: ")
    )

def get_env_info(code):
    """get_env_info"""

    for env in ENV_LIST:
        if env["code"] == int(code):
            return env

    return None

def read_config(env_code):
    """read config"""

    file_name = os.path.join(
        ".",
        "env",
        "{}".format(
            get_env_info(env_code)["filename"]
        )
    )

    print("\nReading {} ...\n".format(file_name))

    with open(file_name, "r") as config_json:
        return json.load(config_json)

def set_path(json_data, path, value):
    """set property in json"""

    if len(path) == 1:
        json_data[path[0]] = value
        return
    return set_path(json_data[path[0]], path[1:], value)

def access_path(json_data, path):
    """get property in json"""

    if len(path) == 0:
        return json_data
    return access_path(json_data[path[0]], path[1:])

def update_json(env_code, config, action_set, new_value):
    """update json file"""

    action_arr = filter(None, action_set.split("."))
    #TODO
    #set_path(...)
    print(action_arr)
    #print(json.dumps(json_data, indent=4, sort_keys=True))

def main():
    """Read info"""

    envs = ""
    for env in [env["name"] + ": " + str(env["code"]) for env in ENV_LIST]:
        envs += "\n{}".format(env)

    env_code = get_info(
        "Please, choose a ENV\n",
        "{}\nCode: ".format(
            envs
        )
    )

    while int(env_code) not in [int(env["code"]) for env in ENV_LIST]:
        env_code = get_info(
            "Error. Please inform a valid ENV code.\n",
            "{}".format(
                envs
            )
        )

    config = read_config(env_code)
    action = show_avaliable_options(config)

    exit_code = 0

    while True:
        if action == exit_code:
            print("Bye.")
            sys.exit(0)
        else:
            action_set = ACTIONS[action -1]["path"]
            new_value = get_info(
                "Editing value for '{}'.".format(action_set), "Value (press enter to finish): "
            )

            update_json(env_code, config, action_set, new_value)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")
