# Copyright (c) 2015 Brett Francis http://www.oort.org
#

import os, sys
import logging
import requests
import json
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache


__version__ = open(os.path.join(os.path.dirname(__file__), '_version')).read()


logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format="%(asctime)s: " + logging.BASIC_FORMAT,
                    datefmt="%Y-%m-%dT%H:%M:%S%z")
logger = logging.getLogger(__name__)

req = CacheControl(requests.Session(), cache=FileCache('pyutu.cache'))

regions = {
    'ap-northeast-1': "Asia Pacific (Tokyo)",
    'ap-southeast-1': "Asia Pacific (Singapore)",
    'ap-southeast-2': "Asia Pacific (Sydney)",
    'eu-central-1': "EU (Frankfurt)",
    'eu-west-1': "EU (Ireland)",
    'sa-east-1': "South America (Sao Paulo)",
    'us-east-1': "US East (N. Virginia)",
    'us-west-1': "US West (N. California)",
    'us-west-2': "US West (Oregon)"
}


svcs = {
    "ec2": {
        'offer_code': "AmazonEC2",
        'prod_families': {
            "Data Transfer": "fromLocation",
            "Compute Instance": "location",
            "IP Address": "location",
            "Dedicated Host": "location"
        }
    },
    "ses": {
        'offer_code': "AmazonSES",
        'prod_families': {
            "Data Transfer": "fromLocation",
            "Sending Email": "location"
        }
    },
    "ddb": {
        'offer_code': "AmazonDynamoDB",
        'prod_families': {
            "Data Transfer": "fromLocation",
            "Database Storage": "location",
            "Provisioned IOPS": "location"
        }
    },
    "s3": {
        'offer_code': "AmazonS3",
        'prod_families': {
            "Data Transfer": "fromLocation",
            "API Request": "location",
            "Storage": "location",
            "Fee": "location"
        }
    }
}
#     "glacier": "AmazonGlacier",
#     "cloudfront": "AmazonCloudFront",
#     "cf": "AmazonCloudFront",
#     "vpc": "AmazonVPC",
#     "kms": "awskms",
#     "rds": "AmazonRDS",
#     "route53": "AmazonRoute53",
#     "r53": "AmazonRoute53",
#     "redshift": "AmazonRedshift",
# }


def check_service(svc):
    if svc not in svcs:
        raise ValueError('Invalid service: {0}'.format(svc))

    return True


def find_price(svc, region, offer_file, terms='OnDemand'):
    check_service(svc=svc)
    products = {}
    for p in offer_file['products']:
        product = offer_file['products'][p]
        prod_fam = product['productFamily']
        if prod_fam in svcs[svc]['prod_families']:
            f2r = svcs[svc]['prod_families'][prod_fam]
            attr_val = product['attributes'][f2r]
            if attr_val == regions[region]:
                sku = product['sku']
                logger.debug('Found product SKU: {0} in region: {1}'.format(
                    sku, region
                ))
                products[sku] = {
                    'offerCode' : offer_file['offerCode'],
                    'product': product,
                    'term': offer_file['terms'][terms][sku]
                }

    return products


class PricingContext(object):

    def __init__(self, region, root="https://pricing.us-east-1.amazonaws.com"):
        self.aws_root = root
        self.region = region
        self.aws_index = self.aws_root + "/offers/v1.0/aws/index.json"
        self._aws_prepend = 'Amazon'
        self.idx = req.get(self.aws_index).json()

    def get_details(self):
        logger.info("Publication Date: {0}".format(self.idx['publicationDate']))
        logger.info("Format Version: {0}".format(self.idx['formatVersion']))

    def get_prices(self, svc, terms='OnDemand'):
        check_service(svc=svc)
        service_alias = svcs[svc]['offer_code']
        logger.info("Service Alias: {0}".format(service_alias))
        url = self.aws_root + \
              self.idx['offers'][service_alias]['currentVersionUrl']

        logger.info("          URL: {0}".format(url))
        logger.info("       Region: {0}".format(self.region))
        offer_file = req.get(url).json()
        prices = find_price(svc, self.region, offer_file)
        logger.info("       Prices:{0}".format(json.dumps(
            prices, indent=2, sort_keys=True))
        )
