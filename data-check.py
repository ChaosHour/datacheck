#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import subprocess
import configparser
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Run data-diff command.')
parser.add_argument('-s', '--source_server', required=True, help='Source server.')
parser.add_argument('-d', '--dest_server', required=True, help='Destination server.')
parser.add_argument('-db', '--dest_db', required=True, help='Destination database.')
parser.add_argument('-t', '--table', required=True, help='Table to compare.')
parser.add_argument('-k', '--primary_key', required=True, help='Primary key column.')
parser.add_argument('-b', '--bisection-factor', type=int, help='Bisection factor.')
parser.add_argument('-th', '--threads', type=int, help='Number of threads.')
args = parser.parse_args()

# Read the username and password from the ~/.my.cnf file
config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.my.cnf'))
#username = config['client']['user']
#password = config['client']['password']
username = config['client_primary1']['user']
password = config['client_primary1']['password']

# Check if the password is enclosed in single quotes
if not (password.startswith("'") and password.endswith("'")):
    # If not, add the single quotes
    password = f"'{password}'"

# Construct the Docker command
command = (
    f"docker run -it data-diff "
    f"mysql://{username}:{password}@{args.source_server}:3306/{args.dest_db} {args.table} "
    f"mysql://{username}:{password}@{args.dest_server}:3307/{args.dest_db} {args.table} "
    f"-k '{args.primary_key}'"
)

# Add optional arguments if they were provided
if args.bisection_factor is not None:
    command += f" --bisection-factor {args.bisection_factor}"
if args.threads is not None:
    command += f" --threads {args.threads}"

# Determine the shell to use based on the operating system
shell = "/bin/bash"  # Default to bash
if platform.system() == "Darwin":  # If the operating system is macOS
    shell = "/bin/zsh"  # Use zsh

# Run the Docker command
subprocess.run(command, shell=True, executable=shell)