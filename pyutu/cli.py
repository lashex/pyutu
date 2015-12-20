#!/usr/bin/env python

import click
import pyutu

pass_pc = click.make_pass_decorator(pyutu.PricingContext, ensure=True)


@click.group()
@click.option('--region', default='us-west-2',
              help='the region from which a price is to be determined')
@click.pass_context
def cli(ctx, region):
    ctx.obj = pyutu.PricingContext(region=region)
    # add a region directly until AWS CLI config integration
    ctx.obj.region = region


@cli.command()
@pass_pc
def index(pc):
    pyutu.get_details(pc)


@cli.command()
@click.argument('service')
@click.option('--sku', default=None, help='a SKU of a product within the given <SERVICE>')
@pass_pc
def price(pc, service, sku):
    pc.sku = sku
    pyutu.get_prices(pc, service.lower())

cli.add_command(index)
cli.add_command(price)

#
# if __name__ == '__main__':
#     cli(obj={})