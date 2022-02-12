#!/usr/bin/python3


from json import load



def get_config(config_file_path):
    '''
    @purpose: load the configuration from the file

    @input: config_file_path: str 

    @returns: config_dict: (

                'REGION':{
                    'SERVICE_NAME': str,
                    'IMAGE_FILTER': str
                }

    ],Regions: str[],Services: str[]
    )

    '''
    config_dict = {}

    with open(config_file_path) as fp:
        config_data = load(fp)
        regions = config_data['regions']
        services = config_data['services']
        for each_region in regions:
            if each_region in config_data:
                config_dict[each_region] = {
                    'SERVICE_NAME': config_data[each_region]['service_name'],
                    'IMAGE_FILTER': config_data[each_region]['images']['filters']

                }
            else:
                config_dict[each_region] = {
                    'SERVICE_NAME': '',
                    'IMAGE_FILTER': {}

                }

    return config_dict, regions, services
