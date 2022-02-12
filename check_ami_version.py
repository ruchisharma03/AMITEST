#!/usr/bin/python3
from os import getenv
from utils.load_config import get_config
from utils.utils import (get_latest_ami_version,
                         get_service_ami_version_from_lc,
                         compare_ami_versions,
                         prepare_boto_clients
                         )

                    
CONFIG_FILE_PATH = getenv('AWS_SERVICE_CONFIG_FILE') # config file path
# check the ami versions
def check_ami_versions():

    result = {}

    config, regions, services = get_config(CONFIG_FILE_PATH)

    boto3_clients = prepare_boto_clients(services, regions)

    for each_region in regions:

        matched = False 
        not_matched = True  

        # boto3 service clients
        ec2_client = boto3_clients[each_region]['EC2']
        autoscaling_client = boto3_clients[each_region]['AUTOSCALING']

        # image filter
        image_filters = config[each_region]['IMAGE_FILTER']
        # service name to filter launch config
        service_name = config[each_region]['SERVICE_NAME']

        # first get the latest ami version
        latest_ami_id = get_latest_ami_version(ec2_client, image_filters)

        # launch config ami id
        launch_config_ami_id = get_service_ami_version_from_lc(
            autoscaling_client, service_name)

        
        # if ami id and launch confi ami id is not None 
        if latest_ami_id and launch_config_ami_id:
            # if ami id matches
            if compare_ami_versions(latest_ami_id, launch_config_ami_id):
                matched = True  
                not_matched = False 
            else:
                matched = False   
                not_matched = True  
        else:
            matched = False 
            not_matched = False  
        
        # store the output
        result[each_region] = {'REGION':  each_region,
               'IMAGE_FILTER': image_filters,
               'SERVICE_NAME': service_name,
               'LATEST_AMI_ID': latest_ami_id,
               'LAUNCH_CONFIG_AMI_ID': launch_config_ami_id,
               'MATCHED': matched,
               'NOT_MATCHED':not_matched

               }
    return result

# get the result in a compact manner
def get_result():
    result = check_ami_versions()
    output  = ''
    for each_region in result:
        if result[each_region]['SERVICE_NAME']:
            output += result[each_region]['SERVICE_NAME'] +":" + str(result[each_region]['MATCHED'])
            output +="," 
    return output

print(get_result())