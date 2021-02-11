import boto3
from botocore.exceptions import ClientError
import logging


class BucketConfig():
    #  def __init__(self, bucket_name, ):
    def list_files(self):
        client = boto3.client('s3')
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file('/tmp/hello.txt', 'mybucket', 'hello.txt')
