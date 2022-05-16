#!/usr/bin/env python3

import time
import sys
import os
import subprocess

OUTPUT_LOGS_PATH = './logs/output.logs'
ERROR_LOGS_PATH = './logs/error.logs'

def main():
    if len(sys.argv) < 2:
        usage()
    
    infos_path = sys.argv[1]
    commands_args = read_slicing_data(infos_path)
    reset_log_files()
    
    for command_args in commands_args:
        config_name = os.path.basename(command_args['config_path'])
        log_message(f"Running slicing for {config_name}")

        stls_path = command_args['stls_path']
        gcodes_path = command_args['gcodes_path']
        config_path = command_args['config_path']

        command = f"bulkslicer --slicer ./PrusaSlicer/prusa-slicer -s {stls_path} -g {gcodes_path} -i {config_path}"
        log_message(f"Command: {command}")
        with open(OUTPUT_LOGS_PATH, 'a') as output_logs, open(ERROR_LOGS_PATH, 'a') as error_logs:
            output_logs.write(f"\n$ {command}")
            subprocess.run(command, shell=True, stdout=output_logs, stderr=error_logs)

        log_message(f"Done")
    
    output_logs.close()
    error_logs.close()

def usage():
    print(f"{sys.argv[0]} <slicing-infos-path>")
    exit()


def read_slicing_data(file_path):
    f = open(file_path, 'r')
    lines = f.readlines()
    f.close()

    return [ 
        {
            'stls_path': line.split(':')[0],
            'gcodes_path': line.split(':')[1],
            'config_path': line.split(':')[2],
        } for line in lines
    ]


def reset_log_files():
    with open(OUTPUT_LOGS_PATH, 'w'), open(ERROR_LOGS_PATH, 'w'):
        pass


def log_message(message):
    hour = time.strftime('%H:%M:%S')
    message = f" [*] {hour} - {message}"
    print(message)


if __name__ == "__main__":
    main()
