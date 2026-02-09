# Platform Engineering CLI Tool

A Python-based Command Line Interface (CLI) for managing AWS resources (S3, EC2, Route53) with built-in governance and tagging standards. This tool acts as a "Self-Service" platform, allowing users to provision resources that are automatically tagged and compliant.

## Features

* **S3:** Create private/public buckets, list user-owned buckets, and upload files.
* **EC2:** Launch t2/t3 instances (Ubuntu/Amazon Linux), stop instances, and enforce strict instance limits (Cap of 2).
* **Route53:** Create Hosted Zones and manage DNS records (A, CNAME, TXT) with UPSERT logic.
* **Governance:**
    * **Region Locking:** Forces all operations to `us-east-1` (N. Virginia).
    * **Auto-Tagging:** Automatically applies `Owner` (Username-Hostname) and `CreatedBy: platform-cli` tags.
    * **Isolation:** Users can only list, stop, or modify resources they created.

## Prerequisites

* Python 3.x
* AWS Credentials (Access Key & Secret Key)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/RomankDevOps/DevOps-Project---Platform-Engineering-CLI-Tool.git
    cd DevOps-Project---Platform-Engineering-CLI-Tool
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure AWS Credentials:**
    The tool uses standard Boto3 configuration. Create a file at `~/.aws/credentials` (Mac/Linux) or `C:\Users\YOUR_NAME\.aws\credentials` (Windows) with the following format:
    ```ini
    [default]
    aws_access_key_id = YOUR_ACCESS_KEY
    aws_secret_access_key = YOUR_SECRET_KEY
    # aws_session_token = YOUR_TOKEN (Only if using Student Labs)
    ```

## Usage

The CLI is hierarchical. Syntax: `python main.py <RESOURCE> <ACTION> [OPTIONS]`

### 1. S3 (Storage)
```bash
# Create a bucket
python main.py s3 create <bucket-name> [--public]

# List your buckets
python main.py s3 list

# Upload a file
python main.py s3 upload <bucket-name> <file-path>
```
### 2. EC2 (Compute)
```bash
# Launch an instance (Enforces limit of 2)
python main.py ec2 create --type t3.micro --os amazon-linux

# List your instances
python main.py ec2 list

# Stop an instance
python main.py ec2 stop <instance-id>
```
### 3. Route53 (DNS)
```bash
# Create a Hosted Zone
python main.py r53 create <domain-name>

# List your zones
python main.py r53 list

# Manage Records (Create/Update/Delete)
python main.py r53 record --zone-id <ID> --name <full-domain> --type <A|CNAME> --value <IP|Target> --action UPSERT
```
## Troubleshooting

If you encounter `NoCredentialsError` or `InvalidClientTokenId` when running the CLI, you can run the included diagnostic script:

```bash

python check_setup.py
