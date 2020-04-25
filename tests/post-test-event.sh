#!/usr/bin/env bash

curl -vX POST https://a1b2c3d4j.execute-api.us-east-1.amazonaws.com/stg/app/store_events -d @tests/aws-api-proxy-header.json --header "x-api-key: api-key-base64"

