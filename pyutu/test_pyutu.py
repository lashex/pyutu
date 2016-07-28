from __future__ import print_function

import pyutu
import unittest
from nose.tools import raises


class PyutuTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class PyutuBadServiceTestCase(PyutuTest):
    @raises(ValueError)
    def test_bad_service(self):
        pc = pyutu.PricingContext(region='us-west-2')
        pc.service = 'ddf'
        pyutu.get_prices(pc)


class PyutuPricingContextTestCase(PyutuTest):

    def test_pc(self):
        pc = pyutu.PricingContext(region='us-west-2')
        pc.terms = 'ondemand'
        pc.service = 'ddb'
        assert pc.terms == 'OnDemand'
        assert pc.service_alias == 'AmazonDynamoDB'

        pc = None
        pc = pyutu.PricingContext(region='us-west-2')
        pc.service = 'ec2'
        pc.add_attributes({
            'operatingSystem': 'Linux',
            'instanceType': 'm4.large'
        })
        assert pc.attributes['operatingSystem'] == 'Linux'
        assert pc.attributes['instanceType'] == 'm4.large'
