#!/usr/bin/env python3

import sys
import argparse
import json
from werkzeug.security import generate_password_hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--password", help="password")
    parser.add_argument("-o", "--origin", help="cross site origin")
    parser.add_argument("-t", "--tokenexp", help="token expiry time", type=int)
    parser.add_argument("--data-location", help="location of task data (default='~/.task'")
    parser.add_argument("--taskrc-location", help="location of taskrc (default='~/.taskrc'")

    args = parser.parse_args()

    config = {}
    if args.password:
        config['PASSWORD'] = args.password
    else:
        config['PASSWORD'] = ''
        while not config['PASSWORD']:
            config['PASSWORD'] = generate_password_hash(input("Enter password: ").strip())

    if args.origin:
        config['CORS_ORIGINS'] = args.origin
    else:
        config['CORS_ORIGINS'] = ''
        while not config['CORS_ORIGINS']:
            config['CORS_ORIGINS'] = input("Enter origin: ").strip() # support comma spaced list

    if args.tokenexp:
        config['TOKEN_EXP'] = args.tokenexp
    else:
        config['TOKEN_EXP'] = ''
        while not config['TOKEN_EXP']:
            try:
                config['TOKEN_EXP'] = int(input("Enter token expiry time (minutes): ").strip())
            except:
                pass

    if args.data_location:
        config['TASKDATA_LOCATION'] = args.data_location
    else:
        taskdata_location = input("Enter alternative taskdata location (blank for default '~/.task'): ").strip() # support comma spaced list
        if taskdata_location:
            config['TASKDATA_LOCATION'] = taskdata_location

    if args.taskrc_location:
        config['TASKRC_LOCATION'] = args.taskrc_location
    else:
        taskrc_location = input("Enter alternative taskrc location (blank for default '~/.taskrc'): ").strip() # support comma spaced list
        if taskrc_location:
            config['TASKRC_LOCATION'] = taskrc_location

    with open('instance/config.json', 'w') as conf_file:
        json.dump(config, conf_file)

if __name__ == "__main__":
    if not sys.version_info.major == 3:
        print("python3 is required")
        sys.exit(1)
    main()
