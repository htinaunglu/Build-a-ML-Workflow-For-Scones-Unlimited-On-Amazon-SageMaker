#Serialize Image Data
import json
import boto3
import base64

s3 = boto3.client('s3')
BUCKET_NAME = 'mybucket696969696969696969696969'
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


# Classification

import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2021-11-14-03-08-32-250"

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['image_data'])
    endpoint = ENDPOINT
    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(
    endpoint,
    sagemaker_session=sagemaker.Session(),
    )

    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")

    # Make a prediction:
    inferences = predictor.predict(image)

    # We return the data back to the Step Function    
    event['inferences'] = inferences.decode('utf-8')
    
    return {
        'statusCode': 200,
        'body': {
            "inferences": event['inferences']
            
        }
    }

# Low Confidence

import json

THRESHOLD = 0.97


def lambda_handler(event, context):
    meets_threshold = None
    # Grab the inferences from the event
    #inferences = ast.literal_eval(event['inferences'])
    inferences = json.loads(event['inferences'])
    # Check if any values in our inferences are above THRESHOLD
    for i in inferences:
        if i > THRESHOLD:
            meets_threshold = True
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

#EOF