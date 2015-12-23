#!/usr/bin/env python

import click
import pyutu
import json
import time

pass_pc = click.make_pass_decorator(pyutu.PricingContext, ensure=True)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
regions = sorted(pyutu.regions.keys())


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--region', default='us-west-2',
              type=click.Choice(regions), show_default=True,
              help='The region from which a price is to be determined.')
@click.option('--terms', type=click.Choice(['ondemand', 'reserved']),
              default="ondemand",
              help='The general payment terms of the product.')
@click.option('--sku', default=None,
              help='A SKU of a product within the given <SERVICE>')
@click.option('--log', default=None,
              type=click.Choice([
                  'INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']),
              help='Set a specific log level')
@click.pass_context
def cli(ctx, region, terms, sku, log):
    ctx.obj = pyutu.PricingContext(region=region)
    ctx.obj.terms = terms
    ctx.obj.sku = sku
    pyutu.set_log_level(level=log)


@cli.command()
@pass_pc
def index(pc):
    pyutu.get_details(pc)


@cli.command()
@click.argument('service')
@click.option('--attrib', '-a', nargs=2, multiple=True,
              type=click.Tuple([str, str]),
              help='An attribute to use as a product filter.')
@pass_pc
def product(pc, service, attrib):
    pc.service = service.lower()
    pc.add_attributes(attribs=attrib)
    click.echo("Service Alias: {0}".format(pc.service_alias))
    click.echo("URL: {0}".format(pc.service_url))
    click.echo("Region: {0}".format(pc.region))
    click.echo("Product Terms: {0}".format(pc.terms))
    click.echo("Filtering Attributes: {0}".format(pc.attributes))

    prods = pyutu.find_products(pc)
    for p in prods:
        click.echo("Product SKU: {0} product: {1}".format(
            p, json.dumps(prods[p], indent=2, sort_keys=True))
        )

    click.echo("Total Products Found: {0}".format(len(prods)))
    click.echo("Time: {0} secs".format(time.process_time()))


@cli.command()
@click.argument('service')
@click.option('--attrib', '-a', nargs=2, multiple=True,
              type=click.Tuple([str, str]),
              help='An attribute to use as a product filter.')
@pass_pc
def price(pc, service, attrib):
    pc.service = service.lower()
    pc.add_attributes(attribs=attrib)
    click.echo("Service Alias: {0}".format(pc.service_alias))
    click.echo("URL: {0}".format(pc.service_url))
    click.echo("Region: {0}".format(pc.region))
    click.echo("Product Terms: {0}".format(pc.terms))
    click.echo("Filtering Attributes: {0}".format(pc.attributes))

    prices = pyutu.get_prices(pc)
    for p in prices:
        click.echo("Rate Code: {0} price: {1}".format(
            p, json.dumps(prices[p], indent=2, sort_keys=True))
        )

    click.echo("Total Prices Found: {0}".format(len(prices)))
    click.echo("Time: {0} secs".format(time.process_time()))

cli.add_command(index)
cli.add_command(product)
