#Serialize Image Data
import json
import boto3
import base64

s3 = boto3.client('s3')
BUCKET_NAME = 'mybucket696969696969696969696969' # bucket name
PREFIX = 'test'
def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event['s3_input_uri']
    bucket = BUCKET_NAME
    # Download the data from s3 to /tmp/image.png
    file_name = '/tmp/image.png'
    ## TODO: fill in
    s3.download_file(bucket,key, file_name)
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }
#EOF