# SSL Expiry

A simple script to check the expiration date on a list of domains.

This simple python 3 utility is meant to be deployed as a cron or run from a lambda service.

## Usage

```sh
$ echo "google.com\nfacebook.com" | python ssl_expiry.py
> google.com cert is fine
> facebook.com cert is fine
```


## Install

Setup your python environment and test it as follows.

```sh
$ conda env create -f environment.yml
$ source activate ssl-expiry
$ echo "google.com\nfacebook.com" | python ssl_expiry.py
```

## AWS API Gateway and Lambda

### AWS Lambda
To deploy to Lambda, create a zip that contains `ssl_expiry.py` and `ssl_expiry_lambda.py` and then follow the normal instructions to setup and configure a Lambda function.  The `ssl_expiry_lambda` will use, if they exist, two env parameters:

- `HOSTLIST`: a comma separated string of hostnames to validate, and
- `EXPIRY_BUFFER`: an int that represents the days prior to expiration that the script will alert for, ie alert if the expiration is within `EXPIRY_BUFFER` days.


### AWS API Gateway
Once the Lambda is configured, you can setup a new api in API Gateway.  The important parts that are not obvious from the API Gateway admin ui are as follows:


You will need to create a new Integration Response for the exception that
is raised when the check finds a failing or soon to fail certificate.

I configured this a  a new Integration Response with a regex of

`.*Cert Errors.*`

and a Body Mapping Template with content type `application/json` and
the template:

```
#set($inputRoot = $input.path('$'))
$input.path('$.errorMessage')
```

With this configuration, the exception raised by the `main` method will
be parsed and returned as the body of the response.  The HTTP status code
will be a 400.

Additionally, in the Method Request section, I declared URL Query String
Parameters for `host_list` and `expiry_buffer`.

Finally, you should also define a Method Response for the 400 status.
This can be left with all for the default empty values for response headers
and response body.