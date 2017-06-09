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

