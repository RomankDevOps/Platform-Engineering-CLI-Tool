import boto3
import click
import os
from utils import get_owner_id, get_standard_tags


@click.group()
def s3():
    """Manage S3 Storage Buckets"""
    pass


@s3.command()
@click.argument('name')
@click.option('--public', is_flag=True, help="Set the bucket to public access.")
def create(name, public):
    """Create a new S3 bucket with standard tags."""
    s3_client = boto3.client('s3')
    tags = get_standard_tags(name)

    # Format tags for S3 'PutBucketTagging' API
    tag_set = [{'Key': t['Key'], 'Value': t['Value']} for t in tags]

    try:
        click.echo(f"Creating bucket '{name}'...")
        s3_client.create_bucket(Bucket=name)

        # Apply standard tags
        s3_client.put_bucket_tagging(
            Bucket=name,
            Tagging={'TagSet': tag_set}
        )

        if public:
            # Note: Account-level Block Public Access must be off for this to work
            s3_client.put_public_access_block(
                Bucket=name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )
            click.echo(f"✓ Bucket created (Public): {name}")
        else:
            click.echo(f"✓ Bucket created (Private): {name}")

    except Exception as e:
        click.echo(f"Error: {e}")


@s3.command()
def list():
    """List only the buckets owned by the current user."""
    s3_client = boto3.client('s3')
    owner_id = get_owner_id()

    try:
        click.echo("Fetching your buckets...")
        response = s3_client.list_buckets()
        found_any = False

        for bucket in response.get('Buckets', []):
            name = bucket['Name']
            try:
                # Fetch tags to verify ownership
                tag_response = s3_client.get_bucket_tagging(Bucket=name)
                tags = tag_response.get('TagSet', [])

                # Check if 'Owner' tag matches
                is_mine = any(t['Key'] == 'Owner' and t['Value'] == owner_id for t in tags)

                if is_mine:
                    click.echo(f" - {name} (Created: {bucket['CreationDate']})")
                    found_any = True
            except:
                continue

        if not found_any:
            click.echo("No platform-cli buckets found for your user.")

    except Exception as e:
        click.echo(f"AWS Error: {e}")


@s3.command()
@click.argument('bucket_name')
@click.argument('file_path')
def upload(bucket_name, file_path):
    """Upload a file to an S3 bucket."""
    s3_client = boto3.client('s3')

    if not os.path.exists(file_path):
        click.echo(f"Error: File '{file_path}' not found.")
        return

    file_name = os.path.basename(file_path)

    try:
        s3_client.upload_file(file_path, bucket_name, file_name)
        click.echo(f"✓ Upload complete: {file_name} -> s3://{bucket_name}/{file_name}")
    except Exception as e:
        click.echo(f"Upload failed: {e}")