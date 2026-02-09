import boto3
import click
from utils import get_owner_id, get_standard_tags


@click.group()
def ec2():
    """Manage EC2 Virtual Machines"""
    pass


@ec2.command()
@click.option('--type', default='t3.micro', help="Instance type (e.g. t3.micro)")
@click.option('--os', default='amazon-linux', type=click.Choice(['amazon-linux', 'ubuntu']), help="Operating System")
def create(type, os):
    """Launch a new EC2 instance (Max limit: 2)."""
    ec2_client = boto3.client('ec2')
    owner_id = get_owner_id()

    # 1. Check current instance count for this user
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'tag:Owner', 'Values': [owner_id]},
                {'Name': 'instance-state-name', 'Values': ['pending', 'running']}
            ]
        )
        current_count = sum(len(r['Instances']) for r in response['Reservations'])

        if current_count >= 2:
            click.echo(f"⛔ Cap Reached: You already have {current_count}/2 instances running.")
            return
    except Exception as e:
        click.echo(f"Error checking quota: {e}")
        return

    # 2. Select AMI (IDs for us-east-1)
    ami_id = ""
    if os == 'amazon-linux':
        ami_id = 'ami-0cff7528ff583bf9a'  # Amazon Linux 2
    elif os == 'ubuntu':
        ami_id = 'ami-042e8287309f5df03'  # Ubuntu 20.04 LTS

    click.echo(f"Launching {os} ({type})...")

    # 3. Launch Instance
    try:
        tags = get_standard_tags(f"vm-{owner_id}")
        # Reformat tags for EC2 structure
        ec2_tags = [{'Key': t['Key'], 'Value': t['Value']} for t in tags]

        response = ec2_client.run_instances(
            ImageId=ami_id,
            InstanceType=type,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': ec2_tags
            }]
        )
        instance_id = response['Instances'][0]['InstanceId']
        click.echo(f"✓ Instance launched: {instance_id}")
    except Exception as e:
        click.echo(f"Launch failed: {e}")


@ec2.command()
def list():
    """List your active instances."""
    ec2_client = boto3.client('ec2')
    owner_id = get_owner_id()

    try:
        response = ec2_client.describe_instances(
            Filters=[{'Name': 'tag:Owner', 'Values': [owner_id]}]
        )

        found = False
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                state = instance['State']['Name']
                iid = instance['InstanceId']
                click.echo(f" - {iid} [{state}]")
                found = True

        if not found:
            click.echo("No instances found.")

    except Exception as e:
        click.echo(f"Error: {e}")


@ec2.command()
@click.argument('instance_id')
def stop(instance_id):
    """Stop an EC2 instance."""
    ec2_client = boto3.client('ec2')
    try:
        ec2_client.stop_instances(InstanceIds=[instance_id])
        click.echo(f"✓ Instance {instance_id} stopped.")
    except Exception as e:
        click.echo(f"Error: {e}")