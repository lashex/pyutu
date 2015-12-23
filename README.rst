pyutu
-----
.. image:: https://img.shields.io/pypi/v/pyutu.svg
   :target: https://pypi.python.org/pypi/pyutu

.. image:: https://img.shields.io/pypi/dm/pyutu.svg
   :target: https://pypi.python.org/pypi/pyutu

.. image:: https://secure.travis-ci.org/lashex/pyutu.png?branch=master
   :target: http://travis-ci.org/lashex/pyutu

A Python-based CLI and library for cloud pricing APIs. Currently covering `AWS Pricing <http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html>`_.

  **utu** – from the Maori_ language, can be a verb that means to repay, pay, ...
.. _Maori: http://maoridictionary.co.nz/word/8937

  **pyutu** – when said fast, sounds like "pay you too" ... which seems appropriate.

Initially, this library just strives to simplify pulling product details and pricing terms from a Service's Offer File for a given Region.

(early) CLI Examples
~~~~~~~~~~~~~~~~~~~~
A CLI example that shows the pricing index file.

.. code-block:: bash

  $> pyutu index
  Publication Date: 2015-12-09T23:40:29Z
  Format Version: v1.0
  Offers: {'AmazonVPC': {'offerCode': 'AmazonVPC', 'currentVersionUrl': '/offers/v1.0/aws/AmazonVPC/current/index.json'}, ...snip...
  ...snip...

A CLI example showing how to get EC2 Linux on-demand prices in the default region for the `m4.large` instance type.

.. code-block:: javascript

  $> pyutu price ec2 -a operatingSystem Linux -a instanceType m4.large
  Service Alias: AmazonEC2
  URL: https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json
  Region: us-west-2
  Product Terms: OnDemand
  Filtering Attributes: {'instanceType': 'm4.large', 'operatingSystem': 'Linux'}
  Price: {'effectiveDate': '2015-12-01T00:00:00Z', 'unit': 'Hrs', 'beginRange': '0', 'sku': 'B2M25Y2U9824Q5TG', 'regionId': 'us-west-2', 'pricePerUnit': {'USD': '0.1260000000'}, 'description': '$0.126 per On Demand Linux m4.large Instance Hour', 'endRange': 'Inf', 'term_description': 'OnDemand'}
  Price: {'effectiveDate': '2015-12-01T00:00:00Z', 'unit': 'Hrs', 'beginRange': '0', 'sku': '8ZSNJR8WJ5729VXM', 'regionId': 'us-west-2', 'pricePerUnit': {'USD': '0.1390000000'}, 'description': '$0.139 per Dedicated Usage Linux m4.large Instance Hour', 'endRange': 'Inf', 'term_description': 'OnDemand'}
  Price: {'effectiveDate': '2015-12-01T00:00:00Z', 'unit': 'Hrs', 'beginRange': '0', 'sku': '62WK2ZX9BN3SYAXW', 'regionId': 'us-west-2', 'pricePerUnit': {'USD': '0.0000000000'}, 'description': '$0.000 per Linux m4.large Dedicated Host Instance hour', 'endRange': 'Inf', 'term_description': 'OnDemand'}
  Total Prices Found: 3

A CLI example showing how to get EC2 Linux product details in the default region for the shared tenancy `m4.large` instance type

.. code-block:: javascript

  $> pyutu product ec2 -a operatingSystem Linux -a instanceType m4.large -a tenancy Shared
  Service Alias: AmazonEC2
  URL: https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json
  Region: us-west-2
  Product Terms: OnDemand
  Filtering Attributes: {'operatingSystem': 'Linux', 'tenancy': 'Shared', 'instanceType': 'm4.large'}
  Product SKU: B2M25Y2U9824Q5TG product: {
    "offerCode": "AmazonEC2",
    "product": {
      "attributes": {
        "clockSpeed": "2.4 GHz",
        "currentGeneration": "Yes",
        "dedicatedEbsThroughput": "450 Mbps",
        "enhancedNetworkingSupported": "Yes",
        "instanceFamily": "General purpose",
        "instanceType": "m4.large",
        "licenseModel": "No License required",
        "location": "US West (Oregon)",
        "locationType": "AWS Region",
        "memory": "8 GiB",
        "networkPerformance": "Moderate",
        "operatingSystem": "Linux",
        "operation": "RunInstances",
        "physicalProcessor": "Intel Xeon E5-2676 v3 (Haswell)",
        "preInstalledSw": "NA",
        "processorArchitecture": "64-bit",
        "processorFeatures": "Intel AVX; Intel AVX2; Intel Turbo",
        "servicecode": "AmazonEC2",
        "storage": "EBS only",
        "tenancy": "Shared",
        "usagetype": "USW2-BoxUsage:m4.large",
        "vcpu": "2"
      },
      "productFamily": "Compute Instance",
      "sku": "B2M25Y2U9824Q5TG"
    },
    "regionId": "us-west-2",
    "term": {
      "B2M25Y2U9824Q5TG.JRTCKXETXF": {
        "effectiveDate": "2015-12-01T00:00:00Z",
        "offerTermCode": "JRTCKXETXF",
        "priceDimensions": {
          "B2M25Y2U9824Q5TG.JRTCKXETXF.6YS6EN2CT7": {
            "appliesTo": [],
            "beginRange": "0",
            "description": "$0.126 per On Demand Linux m4.large Instance Hour",
            "endRange": "Inf",
            "pricePerUnit": {
              "USD": "0.1260000000"
            },
            "rateCode": "B2M25Y2U9824Q5TG.JRTCKXETXF.6YS6EN2CT7",
            "unit": "Hrs"
          }
        },
        "sku": "B2M25Y2U9824Q5TG",
        "termAttributes": {}
      }
    },
    "term_description": "OnDemand"
  }
  Total Products Found: 1
  Time: 5.734775 secs


A CLI example showing how to get all on-demand DDB prices in the default region.

.. code-block:: javascript

  $> pyutu price ddb
  Service Alias: AmazonDynamoDB
  URL: https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonDynamoDB/current/index.json
  Region: us-west-2
  Product Terms: OnDemand
  Filtering Attributes: {}
  Rate Code: VTDJ9RVHJGJP999U.JRTCKXETXF.6YS6EN2CT7 price: {
    "beginRange": "0",
    "description": "$0.00 per GB - US West (Oregon) data transfer from EUC1 (FRA)",
    "effectiveDate": "2015-07-01T00:00:00Z",
    "endRange": "Inf",
    "pricePerUnit": {
      "USD": "0.0000000000"
    },
    "regionId": "us-west-2",
    "sku": "VTDJ9RVHJGJP999U",
    "term_description": "OnDemand",
    "unit": "GB"
  }
      ...snip...
  Total Prices Found: 31
  Time: 0.417241 secs



- [ ] Add ability to find specific product families' prices