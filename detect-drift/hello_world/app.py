import json

import boto3

client = boto3.client('cloudformation')

from datetime import date, datetime

def json_serial(obj):
    """date, datetime conversion function
    """
    # For date type, convert it to a character string
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    # Not supported except above
    raise TypeError ("Type %s not serializable" % type(obj))

def json_dumps(obj):
    return json.dumps(obj, default=json_serial, indent=4, separators=(',', ': '))

def lambda_handler(event, context):

    response = client.describe_stacks()

    stacks = response['Stacks']
    for stack in stacks:
        response = client.describe_stack_resource_drifts(StackName=stack['StackName'])
        for stack_resource_drift in response['StackResourceDrifts']:
            print(stack_resource_drift['StackId'], stack_resource_drift['StackResourceDriftStatus'])

        # print(json_dumps(response))

    return {
        "statusCode": 200,
        "body": json.dumps({
            'message': 'hello world'
        })
    }
