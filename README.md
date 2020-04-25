# sparkpost-message-events-collector

# packaging

uuid is bundled with python since version 2.5, see docs, you should not install it in your virtual environment.
    
    uuid

There is no need to install it, otherwise you might encounter errors like:

    Syntax error in module 'app/*': invalid syntax (uuid.py, line 138)

You can omit a package from deployment with the noDeploy option. Note that dependencies of omitted packages must explicitly be omitted too. By default, the following packages are omitted as they are already installed on Lambda:

    boto3
    botocore
    docutils
    jmespath
    pip
    python-dateutil
    s3transfer
    setuptools
    six

# plugin: https://github.com/UnitedIncome/serverless-python-requirements

#### Decisions:

Every transmission (email message) generates events; when it bounces, gets opened, etc. To store these events in a reasonable manner a few keys need to be elaborated on.

    event_id - Unique event identifier
    message_id - SparkPost-cluster-wide unique identifier for this message
    subaccount_id - Unique subaccount identifier


#### Flow:

1. Generate and deploy stack.
2. A webhook will be set up if one has not been setup. (As of March 2019 - this )
    
** DISCLAIMER **: 
    Sparkpost's ability to configure which subaccounts to tie to a webhook is kind of lacking. It's pretty much a single, master, or master and all subaccounts, but master is for administration purposes, and a single webhook for hundreds or thousands is nerve-wrecking to manage, unless you have a nifty framew0rk.

K.I.S.S - This will store these events in batches.

### AWS

#### Cognito

The Client credentials flow is used in machine-to-machine communications. With it you can request an access token to access your own resources. Use this flow when your app is requesting the token on its own behalf, not on behalf of a user. 

    - Since the client credentials flow is not used on behalf of a user, only custom scopes can be used with this flow.

    - A custom scope is one that you define for your own resource server.

    - The format is `resource-server-identifier/scope`.

### implement auth
- iam policy/role can be added to devs who need access to the functions/REST api paths
- 

## Auth:

The API gateway in this project will generate an API key. This key will be used for a `token` request.

The sparkpost webhook will use a username:password as `Basic Auth` mechanism to store message events in AWS. The Authorization header will be decoded as `username, token` and the token will be validated against the API gateway.




#### References:

1. Amazon Cognito User Pool OAuth 2.0 Grants - https://aws.amazon.com/blogs/mobile/understanding-amazon-cognito-user-pool-oauth-2-0-grants/

2. https://github.com/UnitedIncome/serverless-python-requirements

