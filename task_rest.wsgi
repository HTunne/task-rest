#!/usr/bin/env python3
import os, sys


lib_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(lib_path)
from task_rest import create_app
application = create_app()
