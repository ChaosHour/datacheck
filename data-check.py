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
args = parser.parse_args()

# Read the username and password from the ~/.my.cnf file
config = configparser.ConfigParser()
config.read(os.path.expanduser('~/.my.cnf'))
username = config['client']['user']
password = config['client']['password']

# Check if the password is enclosed in single quotes
if not (password.startswith("'") and password.endswith("'")):
    # If not, add the single quotes
    password = f"'{password}'"


# Construct the Docker command
#print(f"Username: {username}")  # Debugging line
#print(f"Password: {password}")  # Debugging line
command = (
    f"docker run -it data-diff "
    f"mysql://{username}:{password}@{args.source_server}:3306/{args.dest_db} {args.table} "
    f"mysql://{username}:{password}@{args.dest_server}:3306/{args.dest_db} {args.table} "
    f"-k '{args.primary_key}'"
)
#print(f"Command: {command}")  # Debugging line

# Determine the shell to use based on the operating system
shell = "/bin/bash"  # Default to bash
if platform.system() == "Darwin":  # If the operating system is macOS
    shell = "/bin/zsh"  # Use zsh

# Run the Docker command
subprocess.run(command, shell=True, executable=shell)