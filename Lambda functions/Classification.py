# Classification

import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

ENDPOINT = "image-classification-2021-11-14-03-08-32-250" # name of your endpoint to use

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
#EOF