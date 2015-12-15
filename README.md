# pyutu
A Python-based CLI and library for cloud pricing APIs with [AWS Pricing](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html) first

__"utu"__ from the [Maori](http://maoridictionary.co.nz/word/8937) language, can be a verb that means to repay, pay, ...

__pyutu__ – if said fast, sounds like "pay you too" ... which seems appropriate.

## (early) Examples
```
$ pyutu index
Publication Date: 2015-12-09T23:40:29Z
Format Version: v1.0
Offers: {'AmazonVPC': {'offerCode': 'AmazonVPC', 'currentVersionUrl': '/offers/v1.0/aws/AmazonVPC/current/index.json'}, 'AmazonGlacier': {'offerCode': 'AmazonGlacier', 'currentVersionUrl': '/offers/v1.0/aws/AmazonGlacier/current/index.json'}, 'AmazonRDS': {'offerCode': 'AmazonRDS',
...snip...
```
```
$ pyutu price ec2
..just outputting for now...
Service Alias: AmazonEC2
          URL: https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json
       region: TODO
        price: TODO
        ...etc...
```
```
$ pyutu price ses
..just outputting for now...
Service Alias: AmazonSES
          URL: https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonSES/current/index.json
       region: TODO
        price: TODO
        ...etc...
```