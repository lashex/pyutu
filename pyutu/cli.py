from __future__ import print_function
import sys
import json
import time
import click
import pyutu.client as pyutu

pass_pc = click.make_pass_decorator(pyutu.PricingContext, ensure=True)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
regions = sorted(pyutu.regions.keys())
services = sorted(pyutu.svcs.keys())


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--region', default='us-west-2',
              type=click.Choice(regions), show_default=True,
              help='The region from which a price is to be determined.')
@click.option('--terms', type=click.Choice(['ondemand', 'reserved']),
              default="ondemand", show_default=True,
              help='The general payment terms of the product.')
@click.option('--log', default='NOTSET', show_default=True,
              type=click.Choice([
                  'INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL', 'NOTSET']),
              help='Set a specific log level')
@click.pass_context
def cli(ctx, region, terms, log):
    ctx.obj = pyutu.PricingContext(region=region)
    ctx.obj.terms = terms
    pyutu.set_log_level(level=log)


@cli.command()
@pass_pc
def index(pc):
    """
    Show details about the Pricing API Index.
    """
    click.echo("Format Version: {0}".format(pc.idx['formatVersion']))
    click.echo("Publication Date: {0}".format(pc.idx['publicationDate']))
    olist = ''
    for i,o in enumerate(pc.idx['offers']):
        if i < len(pc.idx['offers']) - 1:
            olist += o + ", "
        else:
            olist += o

    click.echo("Services Offered: {0}".format(olist))


@cli.command()
@click.argument('service', type=click.Choice(services))
@click.option('--attrib', '-a', nargs=2, multiple=True,
              type=click.Tuple([str, str]),
              help='One or more attributes to use as a product filter.')
@click.option('--sku', default=None,
              help='Get the SKU of a product within the given <SERVICE>')
@pass_pc
def product(pc, service, attrib, sku):
    """
    Get a list of a service's products.
    The list will be in the given region, matching the specific terms and
    any given attribute filters or a SKU.
    """
    pc.service = service.lower()
    pc.sku = sku
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
@click.argument('service', type=click.Choice(services))
@click.option('--attrib', '-a', nargs=2, multiple=True,
              type=click.Tuple([str, str]),
              help='An attribute to use as a product filter.')
@click.option('--sku', default=None,
              help='Price the SKU of a product within the given <SERVICE>')
@pass_pc
def price(pc, service, attrib, sku):
    """
    Get a list of a service's prices.
    The list will be in the given region, matching the specific terms and
    any given attribute filters or a SKU.
    """
    pc.service = service.lower()
    pc.sku = sku
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
    if sys.version_info >= (3, 3):
        click.echo("Time: {0} secs".format(time.process_time()))

cli.add_command(index)
cli.add_command(product)

if __name__ == '__main__':
    cli()
