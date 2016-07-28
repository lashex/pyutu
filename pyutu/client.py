# Copyright (c) 2016 Brett Francis http://www.oort.org
#

import sys
import logging
import requests
import json
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache


logging.basicConfig(stream=sys.stdout,
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


def camel_case(st):
    output = ''.join(x for x in st.title() if x.isalpha())
    return output[0].lower() + output[1:]


class PricingContext(object):

    def __init__(self, region):
        self.sku = None
        self.aws_root = "https://pricing.us-east-1.amazonaws.com"
        self.region = region
        self.aws_index = self.aws_root + "/offers/v1.0/aws/index.json"
        self.idx = req.get(self.aws_index).json()
        self.sku = None
        self.service = ''
        self._service_alias = None
        self._service_url = None
        self._terms = None
        self.attributes = {}

    @property
    def terms(self):
        if self._terms is None:
            self._terms = "OnDemand"
        return self._terms

    @terms.setter
    def terms(self, value):
        # maps any input value regardless of case to the AWS product term
        term_map = {'ondemand': "OnDemand", "reserved": "Reserved"}
        t = value.lower()
        self._terms = term_map[t]

    @property
    def service_alias(self):
        if self.service == '':
            raise AttributeError('Must set PricingContext.service before'
                                 ' an alias can be determined.')
        if self._service_alias is None:
            self._service_alias = svcs[self.service]['offer_code']

        return self._service_alias

    def add_attributes(self, attribs):
        logger.debug("Adding attribs: {0}".format(attribs))
        self.attributes.update(attribs)

    @property
    def service_url(self):
        if self._service_url is None:
            self._service_url = self.aws_root + \
                  self.idx['offers'][self.service_alias]['currentVersionUrl']
        return self._service_url


def set_log_level(level=None):
    if level:
        logger.setLevel(level=level.upper())


def check_service(service):
    if service not in svcs:
        raise ValueError('Invalid service: {0}'.format(service))

    return True


def find_products(pc):
    check_service(service=pc.service)

    logger.info("Service Alias: {0}".format(pc.service_alias))
    logger.info("URL: {0}".format(pc.service_url))
    logger.info("Region: {0}".format(pc.region))
    logger.info("Product Terms: {0}".format(pc.terms))

    offer_file = req.get(pc.service_url).json()

    products = {}
    if pc.sku is None:
        # find service's product in a region that matches
        # the terms and attributes
        for p in offer_file['products']:
            product = offer_file['products'][p]
            prod_fam = product['productFamily']
            if prod_fam in svcs[pc.service]['prod_families']:
                # Cannot simply use 'region' as an attribute because we need to
                # pick the right regional 'from attribute' by product family
                # AND service
                f2r = svcs[pc.service]['prod_families'][prod_fam]
                attr_val = product['attributes'][f2r]
                if attr_val == regions[pc.region]:
                    sku = product['sku']
                    logger.debug('Found product SKU: {0} in region: {1}'.format(
                        sku, pc.region
                    ))
                    match = _match_terms_attribs(pc, offer_file, product, sku)
                    if match:
                        logger.debug('Product matched attributes: {0}'.format(
                            pc.attributes))
                        products[sku] = match
    else:
        # just try to get the given SKU
        logger.debug('Getting specific product SKU: {0}'.format(pc.sku))
        products[pc.sku] = get_sku(pc)

    if logging.INFO == logger.getEffectiveLevel():
        logger.info("Products: \n{0}".format(json.dumps(
            products, indent=2, sort_keys=True))
        )
    return products


def get_sku(pc):
    offer_file = req.get(pc.service_url).json()

    return {
        'regionId': pc.region,
        'offerCode': offer_file['offerCode'],
        'product': offer_file['products'][pc.sku],
        'term': offer_file['terms'][pc.terms][pc.sku],
        'term_description': pc.terms
    }


def get_prices(pc):
    products = find_products(pc)
    prices = {}
    for p in products:
        offer_term = products[p]['term']
        for ot in offer_term:
            price_dim = offer_term[ot]['priceDimensions']
            for pd in price_dim:
                rc = price_dim[pd]
                rate_code = rc['rateCode']
                prices[rate_code] = {
                    'regionId': pc.region,
                    'unit': rc['unit'], 'pricePerUnit': rc['pricePerUnit'],
                    'description': rc['description'],
                    'sku': offer_term[ot]['sku'],
                    'effectiveDate': offer_term[ot]['effectiveDate'],
                    'term_description': pc.terms
                }
                if 'beginRange' in rc:
                    prices[rate_code].update({
                        'beginRange': rc['beginRange'],
                        'endRange': rc['endRange'],
                    })

    if logging.INFO == logger.getEffectiveLevel():
        logger.info("Prices: \n{0}".format(json.dumps(
            prices, indent=2, sort_keys=True))
        )
    return prices


def _match_terms_attribs(pc, offer_file, product, sku):
    logger.debug('Checking product terms: {0}'.format(pc.terms))
    try:
        terms = offer_file['terms'][pc.terms][sku]
        # checking attributes
        logger.debug('Checking product attributes: {0}'.format(
            pc.attributes
        ))
        if len(pc.attributes) is 0:
            return {
                'regionId': pc.region,
                'offerCode': offer_file['offerCode'],
                'product': product,
                'term': terms,
                'term_description': pc.terms
            }

        if set(pc.attributes.items()) <= set(product['attributes'].items()):
            # every element in the filter attributes set is in the other set
            # so True means all Key and Value pairs match
            return {
                'regionId': pc.region,
                'offerCode': offer_file['offerCode'],
                'product': product,
                'term': terms,
                'term_description': pc.terms
            }
    except KeyError:
        logger.debug("SKU {0} filtered vs. Terms: {1}".format(
            sku, pc.terms))

    return None
