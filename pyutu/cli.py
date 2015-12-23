#!/usr/bin/env python

import click
import pyutu

pass_pc = click.make_pass_decorator(pyutu.PricingContext, ensure=True)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
regions = sorted(pyutu.regions.keys())


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--region', default='us-west-2',
              type=click.Choice(regions),
              help='The region from which a price is to be determined.')
@click.option('--debug', is_flag=True,
              help='Activate debug output for Pyutu.')
@click.pass_context
def cli(ctx, region, debug):
    ctx.obj = pyutu.PricingContext(region=region)
    ctx.obj.region = region
    if debug:
        pyutu.set_debug()


@cli.command()
@pass_pc
def index(pc):
    pyutu.get_details(pc)


@cli.command()
@click.argument('service')
@click.option('--attrib', '-a', nargs=2, multiple=True,
              type=click.Tuple([str, str]),
              help='An attribute to use as a filter.')
@click.option('--terms', type=click.Choice(['ondemand', 'reserved']),
              default="ondemand",
              help='The general payment terms of the product.')
@click.option('--sku', default=None,
              help='A SKU of a product within the given <SERVICE>')
@pass_pc
def price(pc, service, sku, terms, attrib):
    click.echo(">> Attribs: {0}".format(attrib))
    pc.sku = sku
    pc.terms = terms
    pc.attributes = {'transferType': 'InterRegion Outbound'}
    pyutu.get_prices(pc, service.lower())

cli.add_command(index)
cli.add_command(price)
