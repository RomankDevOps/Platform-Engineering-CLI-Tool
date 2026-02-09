import getpass
import socket


def get_owner_id():
    """
    Generates a unique Owner ID string based on the current user and hostname.
    Format: <username>-<hostname>
    """
    try:
        username = getpass.getuser()
        hostname = socket.gethostname()
        return f"{username}-{hostname}"
    except Exception:
        return "unknown-user"


def get_standard_tags(resource_name):
    """
    Generates the standard list of AWS tags required for governance.
    Returns a list of dictionaries: [{'Key': '...', 'Value': '...'}]
    """
    unique_owner_id = get_owner_id()

    tags = [
        {'Key': 'Owner', 'Value': unique_owner_id},
        {'Key': 'CreatedBy', 'Value': 'platform-cli'},
        {'Key': 'Name', 'Value': resource_name}
    ]
    return tags