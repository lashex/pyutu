#!/usr/bin/env python

import click
from pyutu import PricingContext


pass_idx = click.make_pass_decorator(PricingContext, ensure=True)


@click.group()
@click.option('--region', default='us-west-2')
@click.pass_context
def cli(ctx, region):
    ctx.obj = PricingContext(region=region)
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
    idx.get_prices(service.lower())

cli.add_command(index)
cli.add_command(price)

#
# if __name__ == '__main__':
#     cli(obj={})