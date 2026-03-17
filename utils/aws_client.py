import boto3
from os import getenv

def get_s3_client():
    return boto3.client('s3', region_name=getenv('AWS_REGION', 'us-east-1'))

def get_iam_client():
    return boto3.client('iam', region_name=getenv('AWS_REGION', 'us-east-1'))

def get_ec2_client():
    return boto3.client('ec2', region_name=getenv('AWS_REGION', 'us-east-1'))

def get_cloudtrail_client():
    return boto3.client('cloudtrail', region_name=getenv('AWS_REGION', 'us-east-1'))