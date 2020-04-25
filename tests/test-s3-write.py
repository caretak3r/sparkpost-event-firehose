#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import uuid

import boto3
import pandas as pd
from pandas.io.json import json_normalize

# Set environment variables
os.environ['REGION'] = "us-east-1"
REGION = os.environ['REGION']

os.environ['SPARKPOST_S3_BUCKET'] = "stg-sparkpost-data"
BUCKET = os.environ['SPARKPOST_S3_BUCKET']

print(f"Region location: {REGION}")
print(f"Bucket name: {BUCKET}")

# Create a session
session = boto3.Session(
    region_name="us-east-1",
    aws_access_key_id="",
    aws_secret_access_key=""
)

# Create clients
s3 = session.client('s3')


def store_events(event, context):
    """

    :param event: a lambda event received from Invoke API
    :param context: a lambda Context runtime methods and attributes
    :return: dict: {'statusCode': int, 'body': dict}
    """

    # Capture the raw event
    print(f"event: {event})")

    # Only accept JSON
    ct = 'application/json'
    try:
        ct = event['headers']['Content-Type']
    except:
        pass
    if ct != 'application/json':
        return {
            "statusCode": 200,
            "body": "Unsupported content type " + event.headers['Content-Type']
        }

    # Make sure we have a unique batch ID
    batch_id = ''
    try:
        batch_id = event['headers']['X-MessageSystems-Batch-ID']
    except:
        pass
    if batch_id == '':
        batch_id = uuid.uuid4()

    # Base the file name off of the uuid+batch_id
    filename = str(batch_id) + '.json'
    print(f"The file name for this event is: {filename}")

    # read event into a pandas dataframe
    df = ''
    # read event into a pandas dataframe
    try:
        df = pd.DataFrame.from_records(json.loads(event['body']))
    except (KeyError, TypeError) as e:
        print(f"Error: {e}")

    normal = json_normalize(data=df['msys'], record_path='message_event')
    print(normal.head(5))

    #subaccount = map(lambda x: x.strip(), event['body'])
    #print(subaccount)

    # write data frame to json
    #print(f"Putting object in {event['body']['subaccount_id']}/{filename}")
    #s3.put_object(Bucket=BUCKET, Key=f"{event['body']['subaccount_id']}/{filename}", ContentType="application/json", Body=df.to_json())

    #print(f"Getting object")
    #s3.get_object(Bucket=BUCKET, Key=f"{event['body']['subaccount_id']}/{filename}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "batch_id": str(batch_id),
            "bucket": BUCKET,
            "filename": filename
        })
    }


def main():
    print(f"Loading test event...")
    with open('aws-api-proxy-header.json', 'r') as j:
        event = json.load(j)

    print(store_events(event, ''))


if __name__ == '__main__':
    main()
