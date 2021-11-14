# Low Confidence

import json

THRESHOLD = 0.97


def lambda_handler(event, context):
    meets_threshold = None
    # Grab the inferences from the event
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