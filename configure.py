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

    args = parser.parse_args()

    config = {}
    if args.password:
        config['PASSWORD'] = args.password
    else:
        config['PASSWORD'] = ''
        while not config['PASSWORD']:
            config['PASSWORD'] = generate_password_hash(input("Enter password: ").strip())

    if args.origin:
        config['ORIGIN'] = args.origin
    else:
        config['ORIGIN'] = ''
        while not config['ORIGIN']:
            config['ORIGIN'] = input("Enter origin: ").strip() # support comma spaced list

    if args.tokenexp:
        config['TOKENEXP'] = args.tokenexp
    else:
        config['TOKENEXP'] = ''
        while not config['TOKENEXP']:
            try:
                config['TOKENEXP'] = int(input("Enter token expiry time (minutes): ").strip())
            except:
                pass


    with open('instance/config.json', 'w') as conf_file:
        json.dump(config, conf_file)

if __name__ == "__main__":
    if not sys.version_info.major == 3:
        print("python3 is required")
        sys.exit(1)
    main()
