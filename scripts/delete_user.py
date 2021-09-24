#!/usr/bin/env python3

import sys
import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="user")

    args = parser.parse_args()

    with open('instance/config.json', 'r') as conf_file:
        config = json.load(conf_file)

    if args.user:
        user = args.user
    else:
        user = ''
        while not user:
            user = input("Enter username to delete: ").strip()

    config.pop(user)

    with open('instance/config.json', 'w') as conf_file:
        json.dump(config, conf_file)

if __name__ == "__main__":
    if not sys.version_info.major == 3:
        print("python3 is required")
        sys.exit(1)
    main()
