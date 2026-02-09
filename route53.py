import boto3
import click
import time


@click.group()
def route53():
    """Manage Route53 DNS"""
    pass


@route53.command()
@click.argument('domain_name')
def create(domain_name):
    """Create a new Public Hosted Zone."""
    r53 = boto3.client('route53')

    try:
        ref = str(time.time())
        response = r53.create_hosted_zone(
            Name=domain_name,
            CallerReference=ref,
            HostedZoneConfig={'Comment': 'Created by platform-cli'}
        )
        zone_id = response['HostedZone']['Id']
        click.echo(f"✓ Hosted Zone created for {domain_name}. ID: {zone_id}")
    except Exception as e:
        click.echo(f"Error: {e}")


@route53.command()
def list():
    """List all Hosted Zones."""
    r53 = boto3.client('route53')
    try:
        response = r53.list_hosted_zones()
        for zone in response['HostedZones']:
            click.echo(f" - {zone['Name']} (ID: {zone['Id']})")
    except Exception as e:
        click.echo(f"Error: {e}")


@route53.command()
@click.option('--zone-id', required=True, help="Hosted Zone ID")
@click.option('--name', required=True, help="Full domain name")
@click.option('--type', required=True, type=click.Choice(['A', 'CNAME', 'TXT']), help="Record Type")
@click.option('--value', required=True, help="IP address or target domain")
@click.option('--action', default='UPSERT', help="Action: CREATE, DELETE, UPSERT")
def record(zone_id, name, type, value, action):
    """Manage DNS Records (Create/Update/Delete)."""
    r53 = boto3.client('route53')

    change = {
        'Action': action,
        'ResourceRecordSet': {
            'Name': name,
            'Type': type,
            'TTL': 300,
            'ResourceRecords': [{'Value': value}]
        }
    }

    try:
        r53.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={'Changes': [change]}
        )
        click.echo(f"✓ DNS Record {action}: {name} -> {value}")
    except Exception as e:
        click.echo(f"Error: {e}")