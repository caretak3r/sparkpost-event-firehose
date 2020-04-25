#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import uuid

from app.lambda_logger import logger
import boto3
import pandas as pd

# Set environment variables
BUCKET = os.environ['BUCKET']
REGION = os.environ['REGION']

# Create a session
session = boto3.Session(region_name=REGION)

# Create clients
s3 = session.client('s3')


def store_events(event, context):
    """

    :param event: a lambda event received from Invoke API
    :param context: a lambda Context runtime methods and attributes
    :return: dict: {'statusCode': int, 'body': dict}
    """

    # Capture the raw event
    logger.debug(f"event: {event})")

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

    # read event into a pandas dataframe
    df = pd.DataFrame.from_records(json.loads(event['body']))

    # write data frame to json
    s3.put_object(Bucket=BUCKET, Key=filename, ContentType="application/json", Body=df.to_json())

    return {
        "statusCode": 200,
        "body": json.dumps({
            "batch_id": str(batch_id),
            "bucket": BUCKET,
            "filename": filename
        })
    }
