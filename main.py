import os
import click
from s3 import s3
from ec2 import ec2
from route53 import route53

# Enforce 'us-east-1' (N. Virginia) for all operations
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


@click.group()
def cli():
    """
    Platform Engineering CLI Tool

    A tool to manage AWS resources (S3, EC2, Route53) with built-in
    governance and tagging standards.
    """
    pass


cli.add_command(s3)
cli.add_command(ec2)
cli.add_command(route53)

if __name__ == '__main__':
    cli()