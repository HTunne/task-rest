#!/usr/bin/env python3

import sys
import argparse
import getpass
import json
from werkzeug.security import generate_password_hash, check_password_hash


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", help="user")
    parser.add_argument("-p", "--password", help="password")
    parser.add_argument("-o", "--origin", help="cross site origin")
    parser.add_argument("-t", "--tokenexp", help="token expiry time", type=int)
    parser.add_argument("--data-location", help="location of task data (default='~/.task'")
    parser.add_argument("--taskrc-location", help="location of taskrc (default='~/.taskrc'")

    args = parser.parse_args()

    with open('instance/config.json', 'r') as conf_file:
        config = json.load(conf_file)

    print(args.user)

    if args.user:
        user = args.user
    else:
        user = ''
        while not user:
            user = input("Enter username: ").strip()
    
    config[user] = {}

    if args.password:
        config[user]['PASSWORD'] = args.password
    else:
        config[user]['PASSWORD'] = ''
        while not config[user]['PASSWORD']:
            password = generate_password_hash(getpass.getpass(prompt="Enter password: ").strip())

            if check_password_hash(password, getpass.getpass(prompt="Repeat password: ").strip()):
                config[user]['PASSWORD'] = password
            else:
                print('Passwords do not match, please try again...')

    if args.origin:
        config[user]['CORS_ORIGINS'] = args.origin
    else:
        config[user]['CORS_ORIGINS'] = ''
        while not config[user]['CORS_ORIGINS']:
            config[user]['CORS_ORIGINS'] = input("Enter origin: ").strip()

    if args.tokenexp:
        config[user]['TOKEN_EXP'] = args.tokenexp
    else:
        config[user]['TOKEN_EXP'] = ''
        while not config[user]['TOKEN_EXP']:
            try:
                config[user]['TOKEN_EXP'] = int(input("Enter token expiry time (minutes): ").strip())
            except:
                pass

    if args.data_location:
        config[user]['TASKDATA_LOCATION'] = args.data_location
    else:
        taskdata_location = input("Enter alternative taskdata location (blank for default '~/.task'): ").strip()
        if taskdata_location:
            config[user]['TASKDATA_LOCATION'] = taskdata_location

    if args.taskrc_location:
        config[user]['TASKRC_LOCATION'] = args.taskrc_location
    else:
        taskrc_location = input("Enter alternative taskrc location (blank for default '~/.taskrc'): ").strip()
        if taskrc_location:
            config[user]['TASKRC_LOCATION'] = taskrc_location

    with open('instance/config.json', 'w') as conf_file:
        json.dump(config, conf_file)

if __name__ == "__main__":
    if not sys.version_info.major == 3:
        print("python3 is required")
        sys.exit(1)
    main()
