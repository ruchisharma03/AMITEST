#!/usr/bin/python3


from json import load


def get_config(config_file_path):
    '''
    @purpose: load the configuration from the file

    @input: config_file_path: str 

    @returns: config_data

    '''

    with open(config_file_path) as fp:
        config_data = load(fp)
    return config_data
