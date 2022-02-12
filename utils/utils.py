#!/usr/bin/python3
from audioop import reverse
import boto3
from datetime import datetime

def prepare_boto_clients(services, regions):

    '''
    @purpose: prepare the boto3 clients per region and service

    @input: services: str[], list of services
            regions: str[], list of regions

    @returns: {
        region: {
            'EC2': Boto3.Client('ec2',region)
        }
    }: str 

    '''
    boto3_clients = {}  # list to store the boto3 clients for different services and regions
    for each_region in regions:
        each_client = {}
        for each_service in services:
            each_client[each_service.upper()] = boto3.client(
                each_service.lower(), region_name=each_region)
        boto3_clients[each_region] = each_client
    return boto3_clients


def get_latest_ami_version(client, filters):
    '''
    @purpose: get the latest ami from a region based on filters

    @input: client: boto3.Client
            filters: [{Name: str ,Values:[]}]

    @returns: ImageId: str 

    '''
    if filters:
        images = client.describe_images(Filters=filters)
        if images and len(images['Images']):
            images['Images'].sort(key=lambda image: image['CreationDate'],reverse=True)
            return images['Images'][0]['ImageId']
    return None 


def get_service_ami_version_from_lc(client, service_name):
    '''
    @purpose: get the service ami from a launch configuration based on name

    @input: client: boto3.Client
            service_name: str

    @returns: ImageId: str 
    '''
    if service_name:
        launch_configurations = client.describe_launch_configurations()
        if launch_configurations and len(launch_configurations['LaunchConfigurations']):
            launch_configurations = list(filter(lambda lc: lc['LaunchConfigurationName'].find(
                service_name) != -1, launch_configurations['LaunchConfigurations']))
            if len(launch_configurations):
                return launch_configurations[0]['ImageId']
    return None 


def compare_ami_versions(this_ami, that_ami):
    '''
    @purpose: compare the amis

    @input: this_ami: boto3.Client
            that_ami: str

    @returns: boolean 
    '''
    return this_ami == that_ami
