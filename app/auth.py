#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The custom authorizer gets the Authorization header in the incoming event
the contents of the header will be in the authorizationToken key, eg:
{
    "type":"TOKEN",
    "authorizationToken":"Basic Zm1vYmFy1ndNQ1loUGE4TUs5SlFWcGU3dVRqWDVGOEY1MUJXa0Q0YVVGZUI2MnQ=",
    "methodArn":"arn:aws:execute-api:<regionId>:<accountId>:<apiId>/<stage>/<method>/<resourcePath>"
}
"""

import base64
import boto3
from app.lambda_logger import logger


def handler(event, context):
    # Return a policy which allows this user to access to this api
    # this call is cached for all authenticated calls, so we need to give
    # access to the whole api. This could be done by having a policyDocument
    # for each available function, but I don't really care :)
    arn = "%s/*" % "/".join(event["methodArn"].split("/")[0:2])

    # if a basic auth header is set, use that to find the correct user/token
    if "Authorization" in event["headers"]:
        authorizationHeader = event["headers"]["Authorization"]
        b64_token = authorizationHeader.split(" ")[-1]

        # decode the base64 encoded header value
        username, token = base64.b64decode(b64_token).decode("utf-8").split(":")

        # search for the given api key
        client = boto3.client("apigateway")
        response = client.get_api_keys(nameQuery=username, includeValues=True)

        # if no keys found, deny access
        if len(response["items"]) != 1:
            logger.debug("Couldn't find key")
            raise Exception("Unauthorized")

        # if the key value does not match, deny access
        if response["items"][0]["value"] != token:
            logger.debug("Key value mismatch")
            raise Exception("Unauthorized")

    # check if an x-api-token header is set, if so, take it as-is, api gateway
    # will check the validity
    elif "x-api-key" in event["headers"]:
        logger.debug("x-api-key received")
        username = "token"
        token = event["headers"]["x-api-key"]

    # no authentication headers found, deny
    else:
        logger.debug("No authentication header found")
        raise Exception("Unauthorized")

    authResponse = {
        "principalId": username,
        "usageIdentifierKey": token,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", "Effect": "Allow", "Resource": arn}
            ],
        },
    }
    logger.debug("Authentication response: %s" % authResponse)

    return authResponse
