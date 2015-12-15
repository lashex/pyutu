#!/usr/bin/env python

import click
import requests


aliases = {
    "ec2": "AmazonEC2",
    "ses": "AmazonSES",
    "DynamoDB": "AmazonDynamoDB",
    "ddb": "AmazonDynamoDB",
    "glacier": "AmazonGlacier",
    "cloudfront": "AmazonCloudFront",
    "cf": "AmazonCloudFront",
    "vpc": "AmazonVPC",
    "kms": "awskms",
    "rds": "AmazonRDS",
    "route53": "AmazonRoute53",
    "r53": "AmazonRoute53",
    "redshift": "AmazonRedshift",
    "s3": "AmazonS3",
}


class PricingContext(object):

    def __init__(self, root="https://pricing.us-east-1.amazonaws.com"):
        self.aws_root = root
        self.aws_index = self.aws_root + "/offers/v1.0/aws/index.json"
        self._aws_prepend = 'Amazon'
        self.idx = requests.get(self.aws_index).json()

    def get_details(self):
        click.echo("Publication Date: {0}".format(self.idx['publicationDate']))
        click.echo("Format Version: {0}".format(self.idx['formatVersion']))
        click.echo("Offers: {0}".format(self.idx['offers']))

    def get_price(self, svc):
        click.echo("..just outputting for now...")
        click.echo("Service Alias: {0}".format(aliases[svc]))
        url = self.aws_root + self.idx['offers'][aliases[svc]]['currentVersionUrl']
        click.echo("          URL: {0}".format(url))


pass_idx = click.make_pass_decorator(PricingContext, ensure=True)


@click.group()
@click.option('--region', default='us-west-2')
@click.pass_context
def cli(ctx, region):
    ctx.obj = PricingContext()
    # add a region directly until AWS CLI config integration
    ctx.obj.region = region


@cli.command()
@pass_idx
def index(idx):
    idx.get_details()


@cli.command()
@click.argument('service')
@pass_idx
def price(idx, service):
    idx.get_price(service)

cli.add_command(index)
cli.add_command(price)

#
# if __name__ == '__main__':
#     cli(obj={})